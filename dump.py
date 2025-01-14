{
    "created": 1736855968.1715379,
    "duration": 0.3660445213317871,
    "exitcode": 1,
    "root": "/tmp/test_tools",
    "environment": {},
    "summary": {
        "passed": 7,
        "failed": 2,
        "total": 9,
        "collected": 9
    },
    "collectors": [
        {
            "nodeid": "",
            "outcome": "passed",
            "result": [
                {
                    "nodeid": ".",
                    "type": "Dir"
                }
            ]
        },
        {
            "nodeid": "test_tools/test_git.py",
            "outcome": "passed",
            "result": [
                {
                    "nodeid": "test_tools/test_git.py::test_git_version",
                    "type": "Function",
                    "lineno": 7
                },
                {
                    "nodeid": "test_tools/test_git.py::test_git_installation_path",
                    "type": "Function",
                    "lineno": 10
                },
                {
                    "nodeid": "test_tools/test_git.py::test_git_symlink",
                    "type": "Function",
                    "lineno": 14
                }
            ]
        },
        {
            "nodeid": "test_tools/test_maven.py",
            "outcome": "passed",
            "result": [
                {
                    "nodeid": "test_tools/test_maven.py::test_maven_version",
                    "type": "Function",
                    "lineno": 7
                },
                {
                    "nodeid": "test_tools/test_maven.py::test_maven_installation_path",
                    "type": "Function",
                    "lineno": 10
                },
                {
                    "nodeid": "test_tools/test_maven.py::test_maven_symlink",
                    "type": "Function",
                    "lineno": 14
                }
            ]
        },
        {
            "nodeid": "test_tools/test_python.py",
            "outcome": "passed",
            "result": [
                {
                    "nodeid": "test_tools/test_python.py::test_python_version",
                    "type": "Function",
                    "lineno": 7
                },
                {
                    "nodeid": "test_tools/test_python.py::test_python_installation_path",
                    "type": "Function",
                    "lineno": 10
                },
                {
                    "nodeid": "test_tools/test_python.py::test_python_symlink",
                    "type": "Function",
                    "lineno": 14
                }
            ]
        },
        {
            "nodeid": "test_tools",
            "outcome": "passed",
            "result": [
                {
                    "nodeid": "test_tools/test_git.py",
                    "type": "Module"
                },
                {
                    "nodeid": "test_tools/test_maven.py",
                    "type": "Module"
                },
                {
                    "nodeid": "test_tools/test_python.py",
                    "type": "Module"
                }
            ]
        },
        {
            "nodeid": ".",
            "outcome": "passed",
            "result": [
                {
                    "nodeid": "test_tools",
                    "type": "Dir"
                }
            ]
        }
    ],
    "tests": [
        {
            "nodeid": "test_tools/test_git.py::test_git_version",
            "lineno": 7,
            "outcome": "passed",
            "keywords": [
                "test_git_version",
                "test_git.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.0002796368207782507,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.00409141113050282,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.00033420114777982235,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_git.py::test_git_installation_path",
            "lineno": 10,
            "outcome": "failed",
            "keywords": [
                "test_git_installation_path",
                "test_git.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.0001781380269676447,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.002278065076097846,
                "outcome": "failed",
                "crash": {
                    "path": "/tmp/test_tools/test_tools/test_git.py",
                    "lineno": 13,
                    "message": "AssertionError: assert '/usr/bin/git' in '/usr/local/bin/git'\n +  where '/usr/local/bin/git' = <built-in method strip of str object at 0x7ffa432acd50>()\n +    where <built-in method strip of str object at 0x7ffa432acd50> = '/usr/local/bin/git\\n'.strip\n +      where '/usr/local/bin/git\\n' = CompletedProcess(args=['which', 'git'], returncode=0, stdout='/usr/local/bin/git\\n', stderr='').stdout"
                },
                "traceback": [
                    {
                        "path": "/tmp/test_tools/test_tools/test_git.py",
                        "lineno": 13,
                        "message": "AssertionError"
                    }
                ],
                "longrepr": "def test_git_installation_path():\n        result = subprocess.run([\"which\", \"git\"], capture_output=True, text=True)\n>       assert \"/usr/bin/git\" in result.stdout.strip()\nE       AssertionError: assert '/usr/bin/git' in '/usr/local/bin/git'\nE        +  where '/usr/local/bin/git' = <built-in method strip of str object at 0x7ffa432acd50>()\nE        +    where <built-in method strip of str object at 0x7ffa432acd50> = '/usr/local/bin/git\\n'.strip\nE        +      where '/usr/local/bin/git\\n' = CompletedProcess(args=['which', 'git'], returncode=0, stdout='/usr/local/bin/git\\n', stderr='').stdout\n\n/tmp/test_tools/test_tools/test_git.py:13: AssertionError"
            },
            "teardown": {
                "duration": 0.0002522009890526533,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_git.py::test_git_symlink",
            "lineno": 14,
            "outcome": "failed",
            "keywords": [
                "test_git_symlink",
                "test_git.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.0001978620421141386,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.004863683134317398,
                "outcome": "failed",
                "crash": {
                    "path": "/tmp/test_tools/test_tools/test_git.py",
                    "lineno": 17,
                    "message": "AssertionError: assert '/usr/local/bin/git' in '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git'\n +  where '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git' = <built-in method strip of str object at 0x7ffa432c4c70>()\n +    where <built-in method strip of str object at 0x7ffa432c4c70> = '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git\\n'.strip\n +      where '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git\\n' = CompletedProcess(args=['ls', '-l', '/usr/bin/git'], returncode=0, stdout='-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git\\n', stderr='').stdout"
                },
                "traceback": [
                    {
                        "path": "/tmp/test_tools/test_tools/test_git.py",
                        "lineno": 17,
                        "message": "AssertionError"
                    }
                ],
                "longrepr": "def test_git_symlink():\n        result = subprocess.run([\"ls\", \"-l\", \"/usr/bin/git\"], capture_output=True, text=True)\n>       assert \"/usr/local/bin/git\" in result.stdout.strip()\nE       AssertionError: assert '/usr/local/bin/git' in '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git'\nE        +  where '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git' = <built-in method strip of str object at 0x7ffa432c4c70>()\nE        +    where <built-in method strip of str object at 0x7ffa432c4c70> = '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git\\n'.strip\nE        +      where '-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git\\n' = CompletedProcess(args=['ls', '-l', '/usr/bin/git'], returncode=0, stdout='-rwxr-xr-x 1 root root 3845696 Jun  5  2024 /usr/bin/git\\n', stderr='').stdout\n\n/tmp/test_tools/test_tools/test_git.py:17: AssertionError"
            },
            "teardown": {
                "duration": 0.00023586000315845013,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_maven.py::test_maven_version",
            "lineno": 7,
            "outcome": "passed",
            "keywords": [
                "test_maven_version",
                "test_maven.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00019327900372445583,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.2907138920854777,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.000205290038138628,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_maven.py::test_maven_installation_path",
            "lineno": 10,
            "outcome": "passed",
            "keywords": [
                "test_maven_installation_path",
                "test_maven.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00015073618851602077,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.002186552854254842,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.0001589711755514145,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_maven.py::test_maven_symlink",
            "lineno": 14,
            "outcome": "passed",
            "keywords": [
                "test_maven_symlink",
                "test_maven.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00014512217603623867,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.0044408750254660845,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.00016486807726323605,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_python.py::test_python_version",
            "lineno": 7,
            "outcome": "passed",
            "keywords": [
                "test_python_version",
                "test_python.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00016981083899736404,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.004429801134392619,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.00020780391059815884,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_python.py::test_python_installation_path",
            "lineno": 10,
            "outcome": "passed",
            "keywords": [
                "test_python_installation_path",
                "test_python.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00016901502385735512,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.001857209950685501,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.00014401297084987164,
                "outcome": "passed"
            }
        },
        {
            "nodeid": "test_tools/test_python.py::test_python_symlink",
            "lineno": 14,
            "outcome": "passed",
            "keywords": [
                "test_python_symlink",
                "test_python.py",
                "test_tools",
                ""
            ],
            "setup": {
                "duration": 0.00018079602159559727,
                "outcome": "passed"
            },
            "call": {
                "duration": 0.004088423913344741,
                "outcome": "passed"
            },
            "teardown": {
                "duration": 0.0001465741079300642,
                "outcome": "passed"
            }
        }
    ]
}
