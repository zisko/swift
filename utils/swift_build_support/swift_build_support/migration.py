# swift_build_support/migration.py - Migrating build-script -*- python -*-
#
# This source file is part of the Swift.org open source project
#
# Copyright (c) 2014 - 2017 Apple Inc. and the Swift project authors
# Licensed under Apache License v2.0 with Runtime Library Exception
#
# See https://swift.org/LICENSE.txt for license information
# See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
#
# ----------------------------------------------------------------------------
#
# utils/build-script takes arguments for its argument parser, as well as
# arguments that are meant to be passed directly to utils/build-script-impl.
# In order to gradually migrate away from build-script-impl, this module
# provides tools to handle parsing of these args.
#
# ----------------------------------------------------------------------------

import subprocess


def parse_args(parser, argv):
    """
    Parse given argument list with given argparse.ArgumentParser.

    Return a processed arguments object. Any unknown arguments are stored in
    `build_script_impl_args` attribute as a list.
    Ignores '--' to be compatible with old style argument list.

        build-script -RT -- --reconfigure
    """
    args, unknown_args = parser.parse_known_args(
        list(arg for arg in argv if arg != '--'))
    args.build_script_impl_args = unknown_args
    return args


def check_impl_args(build_script_impl, argv):
    """
    Check whether given argv are all known arguments for `build-script-impl`.

    Raise ValueError with message if any invalid argument is found.
    Return nothing if success.
    """
    pipe = subprocess.Popen(
        [build_script_impl, '--check-args-only=1'] + argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    (_, err) = pipe.communicate()

    if pipe.returncode != 0:
        msg = str(err.splitlines()[0].decode())
        raise ValueError(msg)


def add_impl_args_to_parser(parser):
    """
    A temporary place to put all the build-script-impl flags while I rid the
    world of it. These are just pulling all of the flags directly into the
    build-script parser, all of the implementations will be in seperate methods
    below.
    """
    parser.add_argument("--dry-run",
                        help="print the commands that would be executed, but do\
                         not execute them",
                        default=None)
    parser.add_argument("--build-args",
                        help="arguments to the build tool; defaults to -j8 when\
                         CMake generator is ",
                        default=None)
    parser.add_argument("--build-dir",
                        help="out-of-tree build directory; default is in-tree. \
                        **This argument is required**",
                        default=None)
    parser.add_argument("--host-cc",
                        help="the path to CC, the 'clang' compiler for the host\
                         platform. **This argument is required**",
                        default=None)
    parser.add_argument("--host-cxx",
                        help="the path to CXX, the 'clang++' compiler for the \
                        host platform. **This argument is required**",
                        default=None)
    parser.add_argument("--host-lipo",
                        help="the path to lipo for creating universal binaries \
                        on Darwin",
                        default=None)
    parser.add_argument("--host-libtool",
                        help="the path to libtool",
                        default=None)
    parser.add_argument("--darwin-xcrun-toolchain",
                        help="the name of the toolchain to use on Darwin",
                        default="default")
    parser.add_argument("--ninja-bin",
                        help="the path to Ninja tool",
                        default=None)
    parser.add_argument("--cmark-build-type",
                        help="the CMake build variant for CommonMark (Debug, \
                        RelWithDebInfo, Release, MinSizeRel). \
                        Defaults to Debug.",
                        default="Debug")
    parser.add_argument("--lldb-extra-cmake-args",
                        help="extra command line args to pass to lldb cmake",
                        default=None)
    parser.add_argument("--lldb-extra-xcodebuild-args",
                        help="extra command line args to pass to lldb \
                        xcodebuild",
                        default=None)
    parser.add_argument("--lldb-test-cc",
                        help="CC to use for building LLDB testsuite test \
                        inferiors.  Defaults to just-built, in-tree clang. \
                        If 'host-toolchain', sets it to same as host-cc.",
                        default=None)
    parser.add_argument("--lldb-test-with-curses",
                        help="run test lldb test runner using curses terminal \
                        control",
                        default=None)
    parser.add_argument("--lldb-test-swift-only",
                        help="when running lldb tests, only include \
                        Swift-specific tests",
                        default=None)
    parser.add_argument("--lldb-no-debugserver",
                        help="delete debugserver after building it, and don't \
                        try to codesign it",
                        default=None)
    parser.add_argument("--lldb-use-system-debugserver",
                        help="don't try to codesign debugserver, and use the \
                        system's debugserver instead",
                        default=None)
    parser.add_argument("--llvm-build-type",
                        help="the CMake build variant for LLVM and Clang \
                        (Debug, RelWithDebInfo, Release, MinSizeRel).  \
                        Defaults to Debug.",
                        default="Debug")
    parser.add_argument("--swift-build-type",
                        help="the CMake build variant for Swift",
                        default="Debug")
    parser.add_argument("--swift-enable-assertions",
                        help="enable assertions in Swift",
                        default="1")
    parser.add_argument("--swift-analyze-code-coverage",
                        help="Code coverage analysis mode for Swift (false, \
                        not-merged, merged). Defaults to false if the \
                        argument is not present, and not-merged if the \
                        argument is present without a modifier.",
                        default="not-merged")
    parser.add_argument("--swift-tools-enable-lto",
                        help="enable LTO compilation of Swift tools. \
                        *NOTE* This does not include the swift standard \
                        library and runtime. Must be set to one of \
                        'thin' or 'full'",
                        default=None)
    parser.add_argument("--llvm-enable-lto",
                        help="Must be set to one of 'thin' or 'full'",
                        default=None)
    parser.add_argument("--llvm-enable-modules",
                        help="enable building llvm using modules",
                        default="0")
    parser.add_argument("--swift-tools-num-parallel-lto-link-jobs",
                        help="The number of parallel link jobs to use when \
                        compiling swift tools",
                        default=None)
    parser.add_argument("--llvm-num-parallel-lto-link-jobs",
                        help="The number of parallel link jobs to use when \
                        compiling llvm",
                        default=None)
    parser.add_argument("--swift-stdlib-build-type",
                        help="the CMake build variant for Swift",
                        default="Debug")
    parser.add_argument("--swift-stdlib-enable-assertions",
                        help="enable assertions in Swift",
                        default="1")
    parser.add_argument("--swift-stdlib-enable-resilience",
                        help="build the Swift stdlib and overlays with \
                        resilience enabled",
                        default="0")
    parser.add_argument("--swift-stdlib-use-nonatomic-rc",
                        help="build the Swift stdlib and overlays with \
                        nonatomic reference count operations enabled",
                        default="0")
    parser.add_argument("--swift-stdlib-sil-serialize-all",
                        help="build the Swift stdlib and overlays with all \
                        method bodies serialized",
                        default="1")
    parser.add_argument("--lldb-build-type",
                        help="the CMake build variant for LLDB",
                        default="Debug")
    parser.add_argument("--llbuild-build-type",
                        help="the CMake build variant for llbuild",
                        default="Debug")
    parser.add_argument("--foundation-build-type",
                        help="the build variant for Foundation",
                        default="Debug")
    parser.add_argument("--libdispatch-build-type",
                        help="the build variant for libdispatch",
                        default="Debug")
    parser.add_argument("--libicu-build-type",
                        help="the build variant for libicu",
                        default="Debug")
    parser.add_argument("--playgroundlogger-build-type",
                        help="the build variant for PlaygroundLogger",
                        default="Debug")
    parser.add_argument("--playgroundsupport-build-type",
                        help="the build variant for PlaygroundSupport",
                        default="Debug")
    parser.add_argument("--xctest-build-type",
                        help="the build variant for xctest",
                        default="Debug")
    parser.add_argument("--swiftpm-build-type",
                        help="the build variant for swiftpm",
                        default="Debug")
    parser.add_argument("--llbuild-enable-assertions",
                        help="enable assertions in llbuild",
                        default="1")
    parser.add_argument("--enable-asan",
                        help="enable Address Sanitizer",
                        default=None)
    parser.add_argument("--cmake",
                        help="path to the cmake binary",
                        default=None)
    parser.add_argument("--distcc",
                        help="use distcc in pump mode",
                        default=None)
    parser.add_argument("--distcc-pump",
                        help="the path to distcc pump executable. This argument\
                         is required if distcc is set.",
                        default=None)
    parser.add_argument("--build-runtime-with-host-compiler",
                        help="use the host c++ compiler to build everything",
                        default=None)
    parser.add_argument("--cmake-generator",
                        help="kind of build system to generate; see output of \
                        'cmake --help' for choices",
                        default="Unix Makefiles")
    parser.add_argument("--verbose-build",
                        help="print the commands executed during the build",
                        default=None)
    parser.add_argument("--install-prefix",
                        help="installation prefix",
                        default=None)
    parser.add_argument("--toolchain-prefix",
                        help="the path to the .xctoolchain directory that houses\
                         the install prefix path",
                        default=None)
    parser.add_argument("--install-destdir",
                        help="the path to use as the filesystem root for the \
                        installation",
                        default=None)
    parser.add_argument("--install-symroot",
                        help="the path to install debug symbols into",
                        default=None)
    parser.add_argument("--swift-install-components",
                        help="a semicolon-separated list of Swift components to\
                         install",
                        default=None)
    parser.add_argument("--llvm-install-components",
                        help="a semicolon-separated list of LLVM components to \
                        install",
                        default=None)
    parser.add_argument("--installable-package",
                        help="the path to the archive of the installation \
                        directory",
                        default=None)
    parser.add_argument("--test-installable-package",
                        help="whether to run post-packaging tests on the \
                        produced package",
                        default=None)
    parser.add_argument("--reconfigure",
                        help="force a CMake configuration run even if \
                        CMakeCache.txt already exists",
                        default=None)
    parser.add_argument("--swift-primary-variant-sdk",
                        help="default SDK for target binaries",
                        default=None)
    parser.add_argument("--swift-primary-variant-arch",
                        help="default arch for target binaries",
                        default=None)
    parser.add_argument("--skip-build-cmark",
                        help="set to skip building CommonMark",
                        default=None)
    parser.add_argument("--skip-build-llvm",
                        help="set to skip building LLVM/Clang",
                        default=None)
    parser.add_argument("--skip-build-compiler-rt",
                        help="set to skip building Compiler-RT",
                        default=None)
    parser.add_argument("--skip-build-swift",
                        help="set to skip building Swift",
                        default=None)
    parser.add_argument("--skip-build-linux",
                        help="set to skip building Swift stdlibs for Linux",
                        default=None)
    parser.add_argument("--skip-build-freebsd",
                        help="set to skip building Swift stdlibs for FreeBSD",
                        default=None)
    parser.add_argument("--skip-build-cygwin",
                        help="set to skip building Swift stdlibs for Cygwin",
                        default=None)
    parser.add_argument("--skip-build-osx",
                        help="set to skip building Swift stdlibs for OS X",
                        default=None)
    parser.add_argument("--skip-build-ios-device",
                        help="set to skip building Swift stdlibs for iOS \
                        devices (i.e. build simulators only)",
                        default=None)
    parser.add_argument("--skip-build-ios-simulator",
                        help="set to skip building Swift stdlibs for iOS \
                        simulators (i.e. build devices only)",
                        default=None)
    parser.add_argument("--skip-build-tvos-device",
                        help="set to skip building Swift stdlibs for tvOS \
                        devices (i.e. build simulators only)",
                        default=None)
    parser.add_argument("--skip-build-tvos-simulator",
                        help="set to skip building Swift stdlibs for tvOS \
                        simulators (i.e. build devices only)",
                        default=None)
    parser.add_argument("--skip-build-watchos-device",
                        help="set to skip building Swift stdlibs for Apple \
                        watchOS devices (i.e. build simulators only)",
                        default=None)
    parser.add_argument("--skip-build-watchos-simulator",
                        help="set to skip building Swift stdlibs for Apple \
                        watchOS simulators (i.e. build devices only)",
                        default=None)
    parser.add_argument("--skip-build-android",
                        help="set to skip building Swift stdlibs for Android",
                        default=None)
    parser.add_argument("--skip-build-lldb",
                        help="set to skip building LLDB",
                        default=None)
    parser.add_argument("--skip-build-llbuild",
                        help="set to skip building llbuild",
                        default=None)
    parser.add_argument("--skip-build-swiftpm",
                        help="set to skip building swiftpm",
                        default=None)
    parser.add_argument("--skip-build-xctest",
                        help="set to skip building xctest",
                        default=None)
    parser.add_argument("--skip-build-foundation",
                        help="set to skip building foundation",
                        default=None)
    parser.add_argument("--skip-build-libdispatch",
                        help="set to skip building libdispatch",
                        default=None)
    parser.add_argument("--skip-build-libicu",
                        help="set to skip building libicu",
                        default=None)
    parser.add_argument("--skip-build-benchmarks",
                        help="set to skip building Swift Benchmark Suite",
                        default=None)
    parser.add_argument("--skip-build-playgroundlogger",
                        help="set to skip building PlaygroundLogger",
                        default=None)
    parser.add_argument("--skip-build-playgroundsupport",
                        help="set to skip building PlaygroundSupport",
                        default=None)
    parser.add_argument("--skip-test-cmark",
                        help="set to skip testing CommonMark",
                        default=None)
    parser.add_argument("--skip-test-lldb",
                        help="set to skip testing lldb",
                        default=None)
    parser.add_argument("--skip-test-swift",
                        help="set to skip testing Swift",
                        default=None)
    parser.add_argument("--skip-test-llbuild",
                        help="set to skip testing llbuild",
                        default=None)
    parser.add_argument("--skip-test-swiftpm",
                        help="set to skip testing swiftpm",
                        default=None)
    parser.add_argument("--skip-test-xctest",
                        help="set to skip testing xctest",
                        default=None)
    parser.add_argument("--skip-test-foundation",
                        help="set to skip testing foundation",
                        default=None)
    parser.add_argument("--skip-test-libdispatch",
                        help="set to skip testing libdispatch",
                        default=None)
    parser.add_argument("--skip-test-libicu",
                        help="set to skip testing libicu",
                        default=None)
    parser.add_argument("--skip-test-playgroundlogger",
                        help="set to skip testing PlaygroundLogger",
                        default=None)
    parser.add_argument("--skip-test-playgroundsupport",
                        help="set to skip testing PlaygroundSupport",
                        default=None)
    parser.add_argument("--skip-test-linux",
                        help="set to skip testing Swift stdlibs for Linux",
                        default=None)
    parser.add_argument("--skip-test-freebsd",
                        help="set to skip testing Swift stdlibs for FreeBSD",
                        default=None)
    parser.add_argument("--skip-test-cygwin",
                        help="set to skip testing Swift stdlibs for Cygwin",
                        default=None)
    parser.add_argument("--skip-test-osx",
                        help="set to skip testing Swift stdlibs for OS X",
                        default=None)
    parser.add_argument("--skip-test-ios-simulator",
                        help="set to skip testing Swift stdlibs for iOS \
                        simulators (i.e. test devices only)",
                        default=None)
    parser.add_argument("--skip-test-ios-host",
                        help="set to skip testing the host parts of the \
                        iOS toolchain",
                        default=None)
    parser.add_argument("--skip-test-tvos-simulator",
                        help="set to skip testing Swift stdlibs for tvOS \
                        simulators (i.e. test devices only)",
                        default=None)
    parser.add_argument("--skip-test-tvos-host",
                        help="set to skip testing the host parts of the \
                        tvOS toolchain",
                        default=None)
    parser.add_argument("--skip-test-watchos-simulator",
                        help="set to skip testing Swift stdlibs for Apple \
                        watchOS simulators (i.e. test devices only)",
                        default=None)
    parser.add_argument("--skip-test-watchos-host",
                        help="set to skip testing the host parts of the \
                        watchOS toolchain",
                        default=None)
    parser.add_argument("--skip-test-android-host",
                        help="set to skip testing the host parts of the \
                        Android toolchain",
                        default=None)
    parser.add_argument("--validation-test",
                        help="set to run the validation test suite",
                        default="0")
    parser.add_argument("--long-test",
                        help="set to run the long test suite",
                        default="0")
    parser.add_argument("--skip-test-benchmarks",
                        help="set to skip running Swift Benchmark Suite",
                        default=None)
    parser.add_argument("--skip-test-optimized",
                        help="set to skip testing the test suite in \
                        optimized mode",
                        default=None)
    parser.add_argument("--stress-test-sourcekit",
                        help="set to run the stress-SourceKit target",
                        default=None)
    parser.add_argument("--workspace",
                        help="source directory containing llvm, clang, swift",
                        default="${HOME}/src")
    parser.add_argument("--enable-llvm-assertions",
                        help="set to enable llvm assertions",
                        default="1")
    parser.add_argument("--build-llvm",
                        help="set to 1 to build LLVM and Clang",
                        default="1")
    parser.add_argument("--build-swift-tools",
                        help="set to 1 to build Swift host tools",
                        default="1")
    parser.add_argument("--build-swift-dynamic-stdlib",
                        help="set to 1 to build dynamic variants of the Swift \
                        standard library",
                        default=None)
    parser.add_argument("--build-swift-static-stdlib",
                        help="set to 1 to build static variants of the Swift \
                        standard library",
                        default=None)
    parser.add_argument("--build-swift-stdlib-unittest-extra",
                        help="set to 1 to build optional StdlibUnittest \
                        components",
                        default="0")
    parser.add_argument("--build-swift-dynamic-sdk-overlay",
                        help="set to 1 to build dynamic variants of the Swift \
                        SDK overlay",
                        default=None)
    parser.add_argument("--build-swift-static-sdk-overlay",
                        help="set to 1 to build static variants of the Swift \
                        SDK overlay",
                        default=None)
    parser.add_argument("--build-swift-examples",
                        help="set to 1 to build examples",
                        default="1")
    parser.add_argument("--build-swift-remote-mirror",
                        help="set to 1 to build the Swift Remote Mirror \
                        library",
                        default="1")
    parser.add_argument("--build-serialized-stdlib-unittest",
                        help="set to 1 to build the StdlibUnittest module \
                        with -sil-serialize-all",
                        default="0")
    parser.add_argument("--build-sil-debugging-stdlib",
                        help="set to 1 to build the Swift standard library \
                        with -gsil to enable debugging and profiling on SIL \
                        level",
                        default="0")
    parser.add_argument("--check-incremental-compilation",
                        help="set to 1 to compile swift libraries multiple \
                        times to check if incremental compilation works",
                        default="0")
    parser.add_argument("--llvm-include-tests",
                        help="Set to true to generate testing targets for LLVM.\
                         Set to true by default.",
                        default="1")
    parser.add_argument("--swift-include-tests",
                        help="Set to true to generate testing targets for Swift.\
                         This allows the build to proceed when 'test' \
                         directory is missing (required for B&I builds)",
                        default="1")
    parser.add_argument("--native-llvm-tools-path",
                        help="directory that contains LLVM tools that are \
                        executable on the build machine",
                        default=None)
    parser.add_argument("--native-clang-tools-path",
                        help="directory that contains Clang tools that are \
                        executable on the build machine",
                        default=None)
    parser.add_argument("--native-swift-tools-path",
                        help="directory that contains Swift tools that are \
                        executable on the build machine",
                        default=None)
    parser.add_argument("--compiler-vendor",
                        help="compiler vendor name [none,apple]",
                        default="none")
    parser.add_argument("--clang-user-visible-version",
                        help="user-visible version of the embedded Clang and \
                        LLVM compilers",
                        default="4.0.0")
    parser.add_argument("--swift-user-visible-version",
                        help="user-visible version of the Swift language",
                        default="3.1")
    parser.add_argument("--swift-compiler-version",
                        help="string that indicates a compiler version for \
                        Swift",
                        default=None)
    parser.add_argument("--clang-compiler-version",
                        help="string that indicates a compiler version for \
                        Clang",
                        default=None)
    parser.add_argument("--embed-bitcode-section",
                        help="embed an LLVM bitcode section in stdlib/overlay \
                        binaries for supported platforms",
                        default="0")
    parser.add_argument("--darwin-crash-reporter-client",
                        help="whether to enable CrashReporter integration",
                        default=None)
    parser.add_argument("--darwin-stdlib-install-name-dir",
                        help="the directory of the install_name for standard \
                        library dylibs",
                        default=None)
    parser.add_argument("--install-cmark",
                        help="whether to install cmark",
                        default=None)
    parser.add_argument("--install-swift",
                        help="whether to install Swift",
                        default=None)
    parser.add_argument("--install-lldb",
                        help="whether to install LLDB",
                        default=None)
    parser.add_argument("--install-llbuild",
                        help="whether to install llbuild",
                        default=None)
    parser.add_argument("--install-swiftpm",
                        help="whether to install swiftpm",
                        default=None)
    parser.add_argument("--install-xctest",
                        help="whether to install xctest",
                        default=None)
    parser.add_argument("--install-foundation",
                        help="whether to install foundation",
                        default=None)
    parser.add_argument("--install-libdispatch",
                        help="whether to install libdispatch",
                        default=None)
    parser.add_argument("--install-libicu",
                        help="whether to install libicu",
                        default=None)
    parser.add_argument("--install-playgroundlogger",
                        help="whether to install PlaygroundLogger",
                        default=None)
    parser.add_argument("--install-playgroundsupport",
                        help="whether to install PlaygroundSupport",
                        default=None)
    parser.add_argument("--darwin-install-extract-symbols",
                        help="whether to extract symbols with dsymutil during \
                        installations",
                        default=None)
    parser.add_argument("--host-target",
                        help="The host target. LLVM, Clang, and Swift will be \
                        built for this target. The built LLVM and Clang will \
                        be used to compile Swift for the cross-compilation \
                        targets. **This argument is required**",
                        default=None)
    parser.add_argument("--stdlib-deployment-targets",
                        help="space-separated list of targets to configure the \
                        Swift standard library to be compiled or \
                        cross-compiled for",
                        default=None)
    parser.add_argument("--build-stdlib-deployment-targets",
                        help="space-separated list that filters which of the \
                        configured targets to build the Swift standard \
                        library for, or 'all'",
                        default="all")
    parser.add_argument("--cross-compile-hosts",
                        help="space-separated list of targets to cross-compile \
                        host Swift tools for",
                        default=None)
    parser.add_argument("--cross-compile-with-host-tools",
                        help="set to use the clang we build for the host to \
                        then build the cross-compile hosts",
                        default=None)
    parser.add_argument("--cross-compile-install-prefixes",
                        help="semicolon-separated list of install prefixes to \
                        use for the cross-compiled hosts. The list expands, \
                        so if there are more cross-compile hosts than \
                        prefixes, unmatched hosts use the last prefix \
                        in the list",
                        default=None)
    parser.add_argument("--skip-merge-lipo-cross-compile-tools",
                        help="set to skip running merge-lipo after installing \
                        cross-compiled host Swift tools",
                        default=None)
    parser.add_argument("--darwin-deployment-version-osx",
                        help="minimum deployment target version for OS X",
                        default="10.9")
    parser.add_argument("--darwin-deployment-version-ios",
                        help="minimum deployment target version for iOS",
                        default="7.0")
    parser.add_argument("--darwin-deployment-version-tvos",
                        help="minimum deployment target version for tvOS",
                        default="9.0")
    parser.add_argument("--darwin-deployment-version-watchos",
                        help="minimum deployment target version for watchOS",
                        default="2.0")
    parser.add_argument("--extra-cmake-options",
                        help="Extra options to pass to CMake for all targets",
                        default=None)
    parser.add_argument("--extra-swift-args",
                        help="Extra arguments to pass to swift modules which \
                        match regex. Assumed to be a flattened cmake list \
                        consisting of [module_regexp, args, module_regexp, \
                        args, ...]",
                        default=None)
    parser.add_argument("--sil-verify-all",
                        help="If enabled, run the SIL verifier after each \
                        transform when building Swift files during this \
                        build process",
                        default="0")
    parser.add_argument("--swift-enable-ast-verifier",
                        help="If enabled, and the assertions are enabled, \
                        the built Swift compiler will run the AST verifier \
                        every time it is invoked",
                        default="1")
    parser.add_argument("--swift-runtime-enable-leak-checker",
                        help="Enable leaks checking routines in the runtime",
                        default="0")
    parser.add_argument("--use-gold-linker",
                        help="Enable using the gold linker",
                        default=None)
    parser.add_argument("--darwin-toolchain-bundle-identifier",
                        help="CFBundleIdentifier for xctoolchain info plist",
                        default=None)
    parser.add_argument("--darwin-toolchain-display-name",
                        help="Display Name for xctoolcain info plist",
                        default=None)
    parser.add_argument("--darwin-toolchain-display-name-short",
                        help="Display Name with out date for xctoolchain info \
                        plist",
                        default=None)
    parser.add_argument("--darwin-toolchain-name",
                        help="Directory name for xctoolchain",
                        default=None)
    parser.add_argument("--darwin-toolchain-version",
                        help="Version for xctoolchain info plist and installer \
                        pkg",
                        default=None)
    parser.add_argument("--darwin-toolchain-application-cert",
                        help="Application Cert name to codesign xctoolchain",
                        default=None)
    parser.add_argument("--darwin-toolchain-installer-cert",
                        help="Installer Cert name to create installer pkg",
                        default=None)
    parser.add_argument("--darwin-toolchain-installer-package",
                        help="The path to installer pkg",
                        default=None)
    parser.add_argument("--darwin-sdk-deployment-targets",
                        help="semicolon-separated list of triples like \
                        'fookit-ios-9.0;barkit-watchos-9.0'",
                        default="xctest-ios-8.0")
    parser.add_argument("--darwin-overlay-target",
                        help="single overlay target to build, dependencies are \
                        computed later",
                        default=None)
    parser.add_argument("--build-jobs",
                        help="The number of parallel build jobs to use",
                        default=None)
    parser.add_argument("--darwin-toolchain-alias",
                        help="Swift alias for toolchain",
                        default=None)
    parser.add_argument("--android-ndk",
                        help="An absolute path to the NDK that will be used as \
                        a libc implementation for Android builds",
                        default=None)
    parser.add_argument("--android-api-level",
                        help="The Android API level to target when building \
                        for Android. Currently only 21 or above is supported",
                        default=None)
    parser.add_argument("--android-ndk-gcc-version",
                        help="The GCC version to use when building for Android.\
                         Currently only 4.9 is supported",
                        default=None)
    parser.add_argument("--android-icu-uc",
                        help="Path to a directory containing libicuuc.so",
                        default=None)
    parser.add_argument("--android-icu-uc-include",
                        help="Path to a directory containing headers for \
                        libicuuc",
                        default=None)
    parser.add_argument("--android-icu-i18n",
                        help="Path to a directory containing libicui18n.so",
                        default=None)
    parser.add_argument("--android-icu-i18n-include",
                        help="Path to a directory containing headers \
                        libicui18n",
                        default=None)
    parser.add_argument("--android-deploy-device-path",
                        help="Path on an Android device to which built Swift \
                        stdlib products will be deployed",
                        default=None)
    parser.add_argument("--check-args-only",
                        help="set to check all arguments are known. Exit with \
                        status 0 if success, non zero otherwise",
                        default=None)
    parser.add_argument("--common-cmake-options",
                        help="CMake options used for all targets, including \
                        LLVM/Clang",
                        default=None)
    parser.add_argument("--cmark-cmake-options",
                        help="CMake options used for all cmark targets",
                        default=None)
    parser.add_argument("--ninja-cmake-options",
                        help="CMake options used for all ninja targets",
                        default=None)
    parser.add_argument("--foundation-cmake-options",
                        help="CMake options used for all foundation targets",
                        default=None)
    parser.add_argument("--libdispatch-cmake-options",
                        help="CMake options used for all libdispatch targets",
                        default=None)
    parser.add_argument("--libicu-cmake-options",
                        help="CMake options used for all libicu targets",
                        default=None)
    parser.add_argument("--llbuild-cmake-options",
                        help="CMake options used for all llbuild targets",
                        default=None)
    parser.add_argument("--lldb-cmake-options",
                        help="CMake options used for all lldb targets",
                        default=None)
    parser.add_argument("--llvm-cmake-options",
                        help="CMake options used for all llvm targets",
                        default=None)
    parser.add_argument("--ninja-cmake-options",
                        help="CMake options used for all ninja targets",
                        default=None)
    parser.add_argument("--swift-cmake-options",
                        help="CMake options used for all swift targets",
                        default=None)
    parser.add_argument("--swiftpm-cmake-options",
                        help="CMake options used for all swiftpm targets",
                        default=None)
    parser.add_argument("--xctest-cmake-options",
                        help="CMake options used for all xctest targets",
                        default=None)
    parser.add_argument("--playgroundsupport-cmake-options",
                        help="CMake options used for all playgroundsupport \
                        targets",
                        default=None)
    parser.add_argument("--playgroundlogger-cmake-options",
                        help="CMake options used for all playgroundlogger \
                        targets",
                        default=None)
    parser.add_argument("--user-config-args",
                        help="**Renamed to --extra-cmake-options**: \
                        User-supplied arguments to cmake when used to do \
                        configuration.",
                        default=None)
    parser.add_argument("--only-execute",
                        help="Only execute the named action \
                        (see implementation)",
                        default="all")
    parser.add_argument("--llvm-lit-args",
                        help="If set, override the lit args passed to LLVM",
                        default=None)
    parser.add_argument("--clang-profile-instr-use",
                        help="If set, profile file to use for clang PGO",
                        default=None)
    parser.add_argument("--coverage-db",
                        help="If set, coverage database to use when \
                        prioritizing testing",
                        default=None)
    parser.add_argument("--build-toolchain-only",
                        help="If set, only build the necessary tools to \
                        build an external toolchain",
                        default=None)
    parser.add_argument("--skip-local-host-install",
                        help="If we are cross-compiling multiple targets, \
                        skip an install pass locally if the hosts match",
                        default=None)
    parser.add_argument("--swift-runtime-enable-cow-existentials",
                        help="Enable the copy-on-write existential \
                        implementation",
                        default="1")
