🔹 Running: check image existence...
🔹 Running: inspect Docker image...
🔹 Running: get image layers...
🔹 Running: get image digest...
🔹 Running: stop container...
⚠️ Cleanup error: Failed during stop container: Error during stop container: Error response from daemon: No such container: test-container-1738741332

Traceback (most recent call last):
  File "/users/p357341a/git/config/local_collections/devsecops/agent_build/test_scripts/get_image_stat.py", line 245, in <module>
    run_docker_tests(sys.argv[1])
  File "/users/p357341a/git/config/local_collections/devsecops/agent_build/test_scripts/get_image_stat.py", line 110, in run_docker_tests
    image_info = analyze_docker_image(image_name)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/users/p357341a/git/config/local_collections/devsecops/agent_build/test_scripts/get_image_stat.py", line 91, in analyze_docker_image
    "virtual_size": inspect_data[0]["VirtualSize"]
                    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
KeyError: 'VirtualSize'
