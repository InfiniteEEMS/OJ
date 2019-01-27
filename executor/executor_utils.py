import docker
import os, sys
import shutil
import uuid

from docker.errors import APIError
from docker.errors import ContainerError
from docker.errors import ImageNotFound


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = 'ubuntu:onlineoj'


client = docker.from_env()

def wrongAnswer_ReadLog(result,log_file):
    log_content = log_file.readline();
    result['lastInput'] = log_content.split("\n")[0].split(":")[1]
    log_content = log_file.readline();
    result['expectedOutput'] = log_content.split("\n")[0].split(":")[1]
    log_content = log_file.readline();
    result['yourOutput'] = log_content.split(":")[1]


SOURCE_FILE_NAMES = {
    "Java": "Solution.java",
    "Python": "Solution.py",
    "C++": "solution.cpp"
}

BINARY_NAMES = {
    "Java": "Solution",
    "Python": "trySolution.py",
    "C++": "./a.out"
}

BUILD_COMMANDS = {
    "Java": "javac",
    "Python": "python3",
    "c++": "g++"
}

EXECUTE_COMMANDS = {
    "Java": "java",
    "Python": "python3",
    "C++": ""
}



def build_and_run(code, lang, id):

    result = {'status': None}

    #Currently Only Support for Python
    if lang != "Python":
		result["info"] = "Currently Only Support Python"
		return result

    #Currently Only Support for Python
    if id != 1:
		result["info"] = "Currently Only Support Problem 1"
		return result


    random_dir = uuid.uuid4()
    host_store_dir = "%s/tmp/%s" % (CURRENT_DIR, random_dir)
    container_working_dir = "/test/%s" % (random_dir)
    test_case_dir = "%s/trySolution" % (CURRENT_DIR)

    os.makedirs(host_store_dir)


    #write code in json into Solution.py
    with open(os.path.join(test_case_dir, "Solution.py"), 'w') as solution_file:  
        solution_file.write(code)
    

    #copy required 
    file_list = ["Solve1.py","Solution.py","trySolution.py"]
    for file_name in file_list:
        shutil.copy(os.path.join(test_case_dir, file_name) , os.path.join(host_store_dir, file_name))
    


    # compile phase
    try: 
        client.containers.run(
            image=IMAGE_NAME,
            command="%s %s" % (BUILD_COMMANDS[lang], SOURCE_FILE_NAMES[lang]),
            volumes={host_store_dir:{'bind': container_working_dir, 'mode': 'rw'}},
            working_dir=container_working_dir
        )

    except ContainerError as e:

        result['status'] = 'Compile Error'
        result['info'] = str(e.stderr)
        shutil.rmtree(host_store_dir)
        return result
    
    # run test cases
    try:
        log = client.containers.run(
            image=IMAGE_NAME,
            command="%s %s" % (EXECUTE_COMMANDS[lang],  BINARY_NAMES[lang]),
            volumes={host_store_dir:{'bind': container_working_dir, 'mode': 'rw'}},
            working_dir=container_working_dir
        )

        log = str(log)
        result['status'] = "Accepted"

    except ContainerError as e:

        if "WrongAnswerError" in str(e.stderr):
            result['status'] = "Wrong Answer"
            with open("%s/%s" % (host_store_dir, "log.txt" ), 'r') as log_file:  
                wrongAnswer_ReadLog(result,log_file)
            shutil.rmtree(host_store_dir)
            return result

        else:
            result['status'] = "Runtime Error"
            result['info'] = str(e.stderr)
            shutil.rmtree(host_store_dir)
            return result
    
    shutil.rmtree(host_store_dir)
    return result
