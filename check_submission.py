#!/usr/bin/env python
#-*- encoding: utf-8 -*-

def add_commandline_arguments_using(add_argument):
    add_argument(
        "--no-magic",
        action="store_true",
        dest="disable_magic",
        default=False,
        help="disable the use of the magic module even if it's available, and fall back to mimetypes"
    )
    add_argument(
        "--valid-only",
        action="store_true",
        dest="valid_only",
        default=False,
        help="display only the valid submission files"
    )
    add_argument(
        "-d", "--directory",
        dest="directory",
        default=".",
        help="the directory in which to look for submission files to verify"
    )

try:
    import argparse
    def parse_commandline_arguments():
        parser = argparse.ArgumentParser(description="Check a directory for valid submission files")
        add_commandline_arguments_using(parser.add_argument)
        args = parser.parse_args()
        return (
            os.path.abspath(args.directory),
            args.disable_magic,
            args.valid_only
        )
except ImportError:
    import optparse
    def parse_commandline_arguments():
        parser = optparse.OptionParser()
        add_commandline_arguments_using(parser.add_option)
        (options, args) = parser.parse_args()
        return (
            os.path.abspath(options.directory),
            options.disable_magic,
            options.valid_only
        )

try:
    import magic
    mime_type = lambda filename: magic.from_file(filename, mime=True)
except ImportError:
    import mimetypes
    mime_type = lambda filename: mimetypes.guess_type(filename)[0]

import collections
import datetime
import itertools
import glob
import mimetypes
import os.path
import re
import sys
import tarfile
import zipfile

def check_file_types(filenames, disable_magic):
    VALID_FILE_TYPES = (
        "application/x-tar",
        "application/zip",
        "application/x-bzip2",
        "application/x-gzip"
    )
    possibly_valid_files = []
    for filename in filenames:
        try:
            file_type = mime_type(filename) if not disable_magic else mimetypes.guess_type(filename)[0]
            if file_type in VALID_FILE_TYPES:
                possibly_valid_files.append(filename)
        except Exception as e:
            print >>sys.stderr, "Error while checking file '{0}', ignoring... [{1!s}]".format(filename, e)

    return possibly_valid_files


def validate_filenames(filenames):
    VALID_COURSE_PREFIXES = (
        "MRC", "HWSW", "RP", "CTRL"
    )
    VALID_FILE_EXTENSIONS = (
        "PDF", "TXT", "IPYNB", "M", "PY"
    )
    regex = re.compile(
        r"(?P<course_prefix>{0})_(?P<name>[a-z]+)_(?P<date>[0-9]{{8}})(\.(?P<ext1>{1})|/(?P=course_prefix)_(?P=name)(_\w+)?_(?P=date)\.(?P<ext2>{1}))".format(
            "|".join(VALID_COURSE_PREFIXES),
            "|".join(VALID_FILE_EXTENSIONS)
        ),
        re.IGNORECASE
    )
    
    filename_matches = itertools.imap(regex.match, filenames)
    actual_matches = [m.groupdict() for m in filename_matches if m is not None]
    
    def extract_extension(match):
        if "ext1" in match and match["ext1"]:
            return match["ext1"]
        return match["ext2"]
    
    return [
        (
            m["course_prefix"],
            m["date"],
            extract_extension(m)
        )
        for m in actual_matches
    ]


def check_for_required_contents(archive_contents):
    REQUIRED_SUBMISSION_TYPES_BY_COURSE = {
        "MRC": set(["IPYNB", "PDF", "TXT"]),
        "HWSW": set(["PDF", "TXT"]),
        "CTRL": set(["IPYNB", "PDF", "TXT"]),
        "RB": set(["PDF", "TXT"])
    }
    submissions = set()
    course_prefixes = set()
    submission_dates = set()
    for content in archive_contents:
        submission_extension = content[2].upper()
        course_prefix = content[0].upper()
        if course_prefix in REQUIRED_SUBMISSION_TYPES_BY_COURSE:
            submissions.add(submission_extension)
            course_prefixes.add(course_prefix)
            submission_dates.add(content[1])

    if len(course_prefixes) > 1:
        return (False, "archive contents have different course prefix strings")

    if len(submission_dates) > 1:
        return (False, "archive contents have different submission dates")

    now = datetime.datetime.now()
    for submission_date in submission_dates:
        try:
            verified_date = datetime.datetime(
                int(submission_date[:4]),
                int(submission_date[4:6]),
                int(submission_date[6:8])
            )
            if verified_date > now:
                return (
                    False,
                    "invalid submission date '{0}', submission date should " \
                    "be the date of the day the assignment was GIVEN, not " \
                    "the due date".format(submission_date)
                )
        except Exception as e:
            return (False, "invalid submission date: {0} [{1!s}]".format(submission_date, e))

    required_submission_types = REQUIRED_SUBMISSION_TYPES_BY_COURSE[list(course_prefixes)[0]]
    missing_file_types = required_submission_types.difference(submissions)
    if missing_file_types:
        return (False, "missing required files: {0}".format(", ".join(missing_file_types)))

    return (True, None)


def verify_archive(filename):
    try:
        archive_file = None
        if not os.path.isfile(filename):
            return (False, "file is not accessible")

        known_file_readers = [
            zipfile.ZipFile,
            tarfile.open
        ]

        for open_func in known_file_readers:
            try:
                archive_file = open_func(filename)
                break
            except:
                pass
        else:
            return (False, "unknown archive file format")

        archive_filenames = collections.deque()
        archive_folders = collections.deque()
        if hasattr(archive_file, "getmembers"):
            def classify_archive_content(content):
                if content.isfile():
                    archive_filenames.append(content.name)
                elif content.isdir(content):
                    archive_folders.append(content.name)
            map(classify_archive_content, archive_file.getmembers())
        elif hasattr(archive_file, "infolist"):
            def classify_archive_content(content):
                if content.filename.endswith("/"):
                    archive_folders.append(content.filename)
                else:
                    archive_filenames.append(content.filename)
            map(classify_archive_content, archive_file.infolist())
        else:
            return (False, "unknown archive file object: {0!s}".format(archive_file))

        valid_archive_contents = validate_filenames(archive_filenames)
        if not valid_archive_contents:
            failure_reason = "none of the files in the archive matched the filename pattern"
            if archive_folders:
                failure_reason = "{0}, the script found the following folders, though:\r\n\n\t{1}\r\n\n" \
                    "We only support a single nesting level, and the folder name has to be valid according to the course rules".format(
                    failure_reason, "\n\t".join(archive_folders)
                )
            return (False, failure_reason)
        return check_for_required_contents(valid_archive_contents)
    except Exception as e:
        return (False, str(e))
    finally:
        # context management support for tarfile/zipfile appeared in 2.7
        if archive_file is not None:
            archive_file.close()



def check_archive_contents(archive_filenames):
    KNOWN_ARCHIVE_EXTENSIONS = (
        ".ZIP", ".TAR", ".GZ",
        ".TGZ", ".BZ2", ".JAR"
    )

    examined_filenames = []
    for archive_filename in archive_filenames:
        filename, extension = os.path.splitext(archive_filename)
        extension = extension.upper()
        if extension in KNOWN_ARCHIVE_EXTENSIONS:
            try:
                archive_is_valid, failure_reason = verify_archive(archive_filename)
                examined_filenames.append(
                    (archive_is_valid, archive_filename, failure_reason)
                )
            except NotImplementedError:
                print >>sys.stderr,"'{0}' could be valid, but your Python distro does not support this archive type, so I don't know how to check it.".format(archive_filename)
        else:
            print "Ignoring unknown file '{0}' [{1}]".format(archive_filename, extension)

    return examined_filenames

def valid_submissions_in_path(path_to_search, disable_magic=False):
    available_files = glob.glob(os.path.join(path_to_search, "*"))
    possibly_valid_files = check_file_types(available_files, disable_magic)
    examined_files = check_archive_contents(possibly_valid_files)
    return [
        filename
        for (is_valid, filename, _) in examined_files if is_valid
    ]    

if __name__ == "__main__":
    path_to_search, disable_magic, valid_only = parse_commandline_arguments()
    if not os.path.isdir(path_to_search):
        print >>sys.stderr, "'{0}' is not a valid path, exiting".format(path_to_search)
        raise SystemExit(3)

    if not valid_only:
        print "#"*50
        print "Looking for submissions in '{0}' using {1}".format(
            os.path.abspath(path_to_search),
            "magic" if "magic" in sys.modules and not disable_magic else "mimetypes"
        )

    available_files = glob.glob(os.path.join(path_to_search, "*"))
    possibly_valid_files = check_file_types(available_files, disable_magic)

    if not possibly_valid_files and not valid_only:
        print """
        Sorry, '{0}' contains no valid files.
        Remember your submission has to be an archive file.
        We support .tar.gz, .tar.bz2, .jar and .zip archives
        """.format(path_to_search)
        raise SystemExit(1)

    examined_files = check_archive_contents(possibly_valid_files)
    if examined_files:
        valid_files = [
            filename
            for (is_valid, filename, _) in examined_files if is_valid
        ]
        invalid_files = [
            (filename, failure_reason)
            for (is_valid, filename, failure_reason) in examined_files if not is_valid
        ]
        if invalid_files and not valid_only:
            print "\r\nThe following files are invalid:"
            print "{0}\n{0}\r\n".format("!"*50)
            for filename, failure_reason in invalid_files:
                print "\n\t{0}:\n\t\t{1}".format(filename, failure_reason)
            print "\r\n{0}\n{0}\r\n".format("!"*50)

        if valid_files:
            print "\r\nFound the following valid submission files:"
            print "{0}\n{0}\r\n".format("*"*50)
            for valid_file in valid_files:
                print "\n\t{0}".format(valid_file)
            print "\r\n{0}\n{0}\r\n".format("*"*50)


    

