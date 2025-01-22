{
            "nodeid": "test_tools/test_java.py::test_alternative_points_to_correct_version[jar]",
            "lineno": 27,
            "outcome": "passed",
            "keywords": [
                "test_alternative_points_to_correct_version[jar]",
                "parametrize",
                "pytestmark",
                "jar",
                "test_java.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.0001759480219334364,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.00015324284322559834,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.00013637286610901356,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_java.py::test_alternative_executable[java]",
            "lineno": 35,
            "outcome": "failed",
            "keywords": [
                "test_alternative_executable[java]",
                "parametrize",
                "pytestmark",
                "java",
                "test_java.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00016476516611874104,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.04613448306918144,
                "outcome": "failed",
                "crash": {
                    "path": "/tmp/test_tools/test_tools/test_java.py",
                    "lineno": 41,
                    "message": "AssertionError: java -version did not return expected output.\nassert 'java' in 'openjdk version \"11.0.25\" 2024-10-15 lts\\nopenjdk runtime environment (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts)\\nopenjdk 64-bit server vm (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts, mixed mode, sharing)\\n'\n +  where 'openjdk version \"11.0.25\" 2024-10-15 lts\\nopenjdk runtime environment (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts)\\nopenjdk 64-bit server vm (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts, mixed mode, sharing)\\n' = <built-in method lower of str object at 0x7f58fd731430>()\n +    where <built-in method lower of str object at 0x7f58fd731430> = 'openjdk version \"11.0.25\" 2024-10-15 LTS\\nOpenJDK Runtime Environment (Red_Hat-11.0.25.0.9-1) (build 11.0.25+9-LTS)\\nOpenJDK 64-Bit Server VM (Red_Hat-11.0.25.0.9-1) (build 11.0.25+9-LTS, mixed mode, sharing)\\n'.lower"
                },
                "traceback": [
                    {
                        "path": "/tmp/test_tools/test_tools/test_java.py",
                        "lineno": 41,
                        "message": "AssertionError"
                    }
                ],
                "longrepr": "alternative = 'java'\n\n    @pytest.mark.parametrize(\"alternative\", JAVA_ALTERNATIVES)\n    def test_alternative_executable(alternative):\n        \"\"\"Check if the alternative executable runs correctly.\"\"\"\n        try:\n            output = subprocess.check_output([alternative, \"-version\"], stderr=subprocess.STDOUT, text=True)\n>           assert \"java\" in output.lower(), f\"{alternative} -version did not return expected output.\"\nE           AssertionError: java -version did not return expected output.\nE           assert 'java' in 'openjdk version \"11.0.25\" 2024-10-15 lts\\nopenjdk runtime environment (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts)\\nopenjdk 64-bit server vm (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts, mixed mode, sharing)\\n'\nE            +  where 'openjdk version \"11.0.25\" 2024-10-15 lts\\nopenjdk runtime environment (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts)\\nopenjdk 64-bit server vm (red_hat-11.0.25.0.9-1) (build 11.0.25+9-lts, mixed mode, sharing)\\n' = <built-in method lower of str object at 0x7f58fd731430>()\nE            +    where <built-in method lower of str object at 0x7f58fd731430> = 'openjdk version \"11.0.25\" 2024-10-15 LTS\\nOpenJDK Runtime Environment (Red_Hat-11.0.25.0.9-1) (build 11.0.25+9-LTS)\\nOpenJDK 64-Bit Server VM (Red_Hat-11.0.25.0.9-1) (build 11.0.25+9-LTS, mixed mode, sharing)\\n'.lower\n\n/tmp/test_tools/test_tools/test_java.py:41: AssertionError"
            },
            "teardown": {
                "duration": 0.00029824418015778065,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_java.py::test_alternative_executable[javac]",
            "lineno": 35,
            "outcome": "passed",
            "keywords": [
                "test_alternative_executable[javac]",
                "parametrize",
                "pytestmark",
                "javac",
                "test_java.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00023226207122206688,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.1446348219178617,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.00022681709378957748,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_java.py::test_alternative_executable[keytool]",
            "lineno": 35,
            "outcome": "failed",
            "keywords": [
                "test_alternative_executable[keytool]",
                "parametrize",
                "pytestmark",
                "keytool",
                "test_java.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00022303685545921326,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.13558747991919518,
                "outcome": "failed",
                "crash": {
                    "path": "/tmp/test_tools/test_tools/test_java.py",
                    "lineno": 45,
                    "message": "Failed: Error while running keytool: Command '['keytool', '-version']' returned non-zero exit status 1."
                },
                "traceback": [
                    {
                        "path": "/tmp/test_tools/test_tools/test_java.py",
                        "lineno": 45,
                        "message": "Failed"
                    }
                ],
                "longrepr": "alternative = 'keytool'\n\n    @pytest.mark.parametrize(\"alternative\", JAVA_ALTERNATIVES)\n    def test_alternative_executable(alternative):\n        \"\"\"Check if the alternative executable runs correctly.\"\"\"\n        try:\n>           output = subprocess.check_output([alternative, \"-version\"], stderr=subprocess.STDOUT, text=True)\n\n/tmp/test_tools/test_tools/test_java.py:40: \n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ \n/usr/lib64/python3.11/subprocess.py:466: in check_output\n    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ \n\ninput = None, capture_output = False, timeout = None, check = True\npopenargs = (['keytool', '-version'],)\nkwargs = {'stderr': -2, 'stdout': -1, 'text': True}\nprocess = <Popen: returncode: 1 args: ['keytool', '-version']>\nstdout = 'Illegal option:  -version\\nKey and Certificate Management Tool\\n\\nCommands:\\n\\n -certreq            Generates a certi...ommand_name --help\" for usage of command_name.\\nUse the -conf <url> option to specify a pre-configured options file.\\n'\nstderr = None, retcode = 1\n\n    def run(*popenargs,\n            input=None, capture_output=False, timeout=None, check=False, **kwargs):\n        \"\"\"Run command with arguments and return a CompletedProcess instance.\n    \n        The returned instance will have attributes args, returncode, stdout and\n        stderr. By default, stdout and stderr are not captured, and those attributes\n        will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them,\n        or pass capture_output=True to capture both.\n    \n        If check is True and the exit code was non-zero, it raises a\n        CalledProcessError. The CalledProcessError object will have the return code\n        in the returncode attribute, and output & stderr attributes if those streams\n        were captured.\n    \n        If timeout is given, and the process takes too long, a TimeoutExpired\n        exception will be raised.\n    \n        There is an optional argument \"input\", allowing you to\n        pass bytes or a string to the subprocess's stdin.  If you use this argument\n        you may not also use the Popen constructor's \"stdin\" argument, as\n        it will be used internally.\n    \n        By default, all communication is in bytes, and therefore any \"input\" should\n        be bytes, and the stdout and stderr will be bytes. If in text mode, any\n        \"input\" should be a string, and stdout and stderr will be strings decoded\n        according to locale encoding, or by \"encoding\" if set. Text mode is\n        triggered by setting any of text, encoding, errors or universal_newlines.\n    \n        The other arguments are the same as for the Popen constructor.\n        \"\"\"\n        if input is not None:\n            if kwargs.get('stdin') is not None:\n                raise ValueError('stdin and input arguments may not both be used.')\n            kwargs['stdin'] = PIPE\n    \n        if capture_output:\n            if kwargs.get('stdout') is not None or kwargs.get('stderr') is not None:\n                raise ValueError('stdout and stderr arguments may not be used '\n                                 'with capture_output.')\n            kwargs['stdout'] = PIPE\n            kwargs['stderr'] = PIPE\n    \n        with Popen(*popenargs, **kwargs) as process:\n            try:\n                stdout, stderr = process.communicate(input, timeout=timeout)\n            except TimeoutExpired as exc:\n                process.kill()\n                if _mswindows:\n                    # Windows accumulates the output in a single blocking\n                    # read() call run on child threads, with the timeout\n                    # being done in a join() on those threads.  communicate()\n                    # _after_ kill() is required to collect that and add it\n                    # to the exception.\n                    exc.stdout, exc.stderr = process.communicate()\n                else:\n                    # POSIX _communicate already populated the output so\n                    # far into the TimeoutExpired exception.\n                    process.wait()\n                raise\n            except:  # Including KeyboardInterrupt, communicate handled that.\n                process.kill()\n                # We don't call process.wait() as .__exit__ does that for us.\n                raise\n            retcode = process.poll()\n            if check and retcode:\n>               raise CalledProcessError(retcode, process.args,\n                                         output=stdout, stderr=stderr)\nE               subprocess.CalledProcessError: Command '['keytool', '-version']' returned non-zero exit status 1.\n\n/usr/lib64/python3.11/subprocess.py:571: CalledProcessError\n\nDuring handling of the above exception, another exception occurred:\n\nalternative = 'keytool'\n\n    @pytest.mark.parametrize(\"alternative\", JAVA_ALTERNATIVES)\n    def test_alternative_executable(alternative):\n        \"\"\"Check if the alternative executable runs correctly.\"\"\"\n        try:\n            output = subprocess.check_output([alternative, \"-version\"], stderr=subprocess.STDOUT, text=True)\n            assert \"java\" in output.lower(), f\"{alternative} -version did not return expected output.\"\n        except FileNotFoundError:\n            pytest.fail(f\"{alternative} is not executable or not found in PATH.\")\n        except subprocess.CalledProcessError as e:\n>           pytest.fail(f\"Error while running {alternative}: {e}\")\nE           Failed: Error while running keytool: Command '['keytool', '-version']' returned non-zero exit status 1.\n\n/tmp/test_tools/test_tools/test_java.py:45: Failed"
            },
            "teardown": {
                "duration": 0.000325558939948678,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_java.py::test_alternative_executable[jar]",
            "lineno": 35,
            "outcome": "failed",
            "keywords": [
                "test_alternative_executable[jar]",
                "parametrize",
                "pytestmark",
                "jar",
                "test_java.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00024627591483294964,
                "outcome": "passed"
