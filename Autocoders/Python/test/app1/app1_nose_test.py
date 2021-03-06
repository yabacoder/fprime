import os
import subprocess
from subprocess import CalledProcessError

import pexpect
from pexpect import TIMEOUT


def a_make_test():

    if make():
        assert True
    else:
        assert False


def b_make_ut_test():

    if make_ut():
        assert True
    else:
        assert False


def c_port_send_test():
    cn = 10
    cs = "Some_String"
    expect_string = r".*\*\*\* Huey: cmd = {cmd_number} str = {cmd_string}.*".format(
        cmd_number=cn, cmd_string=cs
    )
    print(expect_string)
    try:
        p = pexpect.spawn("make run_ut")
        p.expect(".*q to quit:.*", timeout=3)
        p.sendline("g")
        p.expect(".*cmd number:.*", timeout=3)
        p.sendline("10")
        p.expect(".*short string:.*", timeout=3)
        p.sendline("Some_String")
        p.expect(r".*\(huey or duey\):.*", timeout=3)
        p.sendline("huey")
        p.expect(expect_string, timeout=5)
        p.expect(".*q to quit:.*", timeout=3)
        p.sendline("q")
        assert True
    except TIMEOUT as e:
        print("Timeout Error. Expected Value not returned.")
        print("-------Program Output-------")
        print(p.before)
        print("-------Expected Output-------")
        print(e.get_trace())
        assert False


def setup_module():
    os.chdir(
        "{BUILD_ROOT}/Autocoders/Python/test/app1".format(
            BUILD_ROOT=os.environ.get("BUILD_ROOT")
        )
    )

    make()
    make_ut()


def teardown_module():

    cleanCmds = ["make clean", "make ut_clean"]
    for cmd in cleanCmds:
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            print("MAKE CLEAN ERROR")
            print("''''''''''''''''")
            print(e.output)
    os.chdir(
        "{BUILD_ROOT}/Autocoders/Python/test".format(
            BUILD_ROOT=os.environ.get("BUILD_ROOT")
        )
    )


def make():
    try:
        subprocess.check_output("make", stderr=subprocess.STDOUT, shell=True)
        return True
    except CalledProcessError as e:
        print("MAKE ERROR")
        print("''''''''''")
        print(e.output)
        return False


def make_ut():
    try:
        subprocess.check_output("make ut", stderr=subprocess.STDOUT, shell=True)
        return True
    except CalledProcessError as e:
        print("MAKE UT ERROR")
        print("'''''''''''''")
        print(e.output)
        return False
