Traceback (most recent call last):
  File "/users/p357341a/git/config/local_collections/devsecops/agent_build/test_scripts/get_image_stat.py", line 135, in <module>
    run_docker_tests(docker_image_name)
  File "/users/p357341a/git/config/local_collections/devsecops/agent_build/test_scripts/get_image_stat.py", line 62, in run_docker_tests
    inspect_docker_image(image_name)
  File "/users/p357341a/git/config/local_collections/devsecops/agent_build/test_scripts/get_image_stat.py", line 28, in inspect_docker_image
    image_details = image_info[0]  # Since the result is an array with a single element
                    ~~~~~~~~~~^^^
KeyError: 0
