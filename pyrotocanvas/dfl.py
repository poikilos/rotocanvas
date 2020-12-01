#!/usr/bin/env python
"""
Command DeepFace Lab automatically.
"""
import os
import shutil
import platform
import subprocess

from threading import Thread
"""
from subprocess import PIPE, Popen
# import fcntl # not available on Windows
from threading  import Thread
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, state, isStdErr):
    for line in iter(out.readline, b''):
        state._q.put(line)
    out.close()

# ^
# as per jfs's Feb 4 '11 at 9:14 answer
# on <https://stackoverflow.com/questions/375427/a-non-blocking-read-on-
# a-subprocess-pipe-in-python>
# edited Aug 6 '18 at 15:02 by ankostis

"""
dflDir = "C:\\PortableApps\\DeepFaceLab\\DeepFaceLab_NVIDIA"
dflWorkspace = os.path.join(dflDir, "workspace")

dfl_params = {
    "source": "Choose the video with the face you want to add.",
    "destination": "Choose the video with the face you want to affect."
}


dfl_install_help_fmt = """
You must install DeepFace Lab such that {} exists.
Visit https://github.com/iperov/DeepFaceLab and scroll down to
"Releases". The magnet link requires a program such as Deluge (free)
from https://dev.deluge-torrent.org/wiki/Download.
"""

dfl_help_fmt = """
After choosing a source and destination, you must run each batch
file in {} in the numbered order.

See also:

"The DeepFaceLab Tutorial (always up-to-date)":
https://pub.dfblue.com/pub/2019-10-25-deepfacelab-tutorial

"DeepFake Tutorial: A beginners Guide with DeepFace Lab":
https://www.cinecom.net/post-production/deepfake-tutorial-beginners/
"""

digits = "0123456789"

def __nonBlockReadline(output):
    # fcntl is NOT AVAILABLE ON WINDOWS
    # so use enqueue_output instead
    try:
        import fcntl
    except ImportError:
        raise EnvironmentError("fcntl is not available")
    # as per John Doe's Dec 13 '11 at 20:46 answer
    # edited Dec 13 '11 at 21:15
    # on <https://stackoverflow.com/questions/8495794/python-popen-
    # stdout-readline-hangs>
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.readline()
    except:
        return ''

class DFL:
    def __init__(self, dflDir):
        self.setDFLDir(dflDir)
        self._cmdDone = True
        self._runCmd = None

        self.prompts = []
        self.prompts.append(" : ")

        self.promptEnds = []
        self.promptEnds.append("? : ")

        self.deadFlags = []
        self.deadFlags.append("above this error message"
                              " when asking for help")

        self._continuePrompts = []
        self._continuePrompts.append("to continue")
        self._continuePrompts.append("Done.")

    def setDFLDir(self, dflDir):
        self._dflDir = dflDir
        self.generateEnv()

    def any_in(self, needles, haystack):
        for needle in needles:
            if needle in haystack:
                return True
        return False

    def generateEnv(self):
        """
        Mimic DeepFaceLab\_internals\setenv.bat but generate
        self.env instead of setting environment variables.
        Always use getenv to use the variables to run another file.
        """
        env = {}
        self.env = env

        # Base env
        env["~dp0"] = dflDir  # if playing this back, do os.chdir(v)
        if not env["~dp0"].endswith(os.sep):
            env["~dp0"] += os.sep
        env["INTERNAL"] = os.path.join(self._dflDir, "_internal")
        if not os.path.isdir(env["INTERNAL"]):
            raise ValueError("{} does not exist. You must provide a"
                             " valid DeepFaceLabs directory."
                             "".format(env["INTERNAL"]))
        intl = env["INTERNAL"]
        env["LOCALENV_DIR"] = os.path.join(intl, "_e")
        le = env["LOCALENV_DIR"]
        env["TMP"] = os.path.join(le, "t")
        env["TEMP"] = os.path.join(le, "t")
        env["HOME"] = os.path.join(le, "u")
        env["HOMEPATH"] = os.path.join(le, "u")
        env["USERPROFILE"] = os.path.join(le, "u")
        env["LOCALAPPDATA"] = os.path.join(env["USERPROFILE"],
                                           "AppData", "Local")
        env["APPDATA"] = os.path.join(env["USERPROFILE"],
                                      "AppData", "Roaming")

        # Python env
        # env["PYTHON_PATH"] = os.path.join(intl, "python-3.6.8")
        pythons = []
        for sub in os.listdir(intl):
            subPath = os.path.join(intl, sub)
            if not os.path.isdir(subPath):
                continue
            if sub.startswith("python"):
                pythons.append(sub)  # Dir NOT exe
        env["PYTHON_PATH"] = os.path.join(intl, pythons[0])
        if len(pythons) > 1:
            print("WARNING: You have more than one python* in {}"
                  "(chose {}): {}"
                  "".format(intl, env["PYTHON_PATH"], pythons))

        env["PYTHONHOME"] = None
        env["PYTHONPATH"] = None
        # ^ Avoid interfering with the default python.
        pydir = env["PYTHON_PATH"]
        py_exe = "python"
        pyw_exe = "pythonw"
        if platform.system() == "Windows":
            py_exe = "python.exe"
            pyw_exe = "pythonw.exe"
        env["PYTHONEXECUTABLE"] = os.path.join(pydir, py_exe)
        env["PYTHONWEXECUTABLE"] = os.path.join(pydir, pyw_exe)
        env["PYTHON_EXECUTABLE"] = os.path.join(pydir, py_exe)
        env["PYTHONW_EXECUTABLE"] = os.path.join(pydir, pyw_exe)
        env["PYTHON_BIN_PATH"] = env["PYTHON_EXECUTABLE"]
        env["PYTHON_LIB_PATH"] = os.path.join(pydir, "Lib",
                                              "site-packages")
        env["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
            env["PYTHON_LIB_PATH"],
            "PyQt5",
            "Qt",
            "plugins"
        )
        self._morePaths = [pydir, os.path.join(pydir, "Scripts")]

        # CUDA Env
        self._morePaths = [os.path.join(intl, "CUDA")] + self._morePaths
        wholeV = platform.uname().version
        parts = wholeV.split(".")
        v = ".".join(parts[:2])
        cudaVerSub = None
        if v == "10.0":
            cudaVerSub = "Win10.0"
        else:
            cudaVerSub = "Win6.x"
        env["V"] = v
        self._morePaths = (
            [os.path.join(intl, "CUDNN", cudaVerSub)] + self._morePaths
        )

        # Additional env
        env["XNVIEWMP_PATH"] = os.path.join(intl, "XnViewMP")
        env["FFMPEG_PATH"] = os.path.join(intl, "ffmpeg")
        self._morePaths = (
            [env["XNVIEWMP_PATH"], env["FFMPEG_PATH"]] + self._morePaths
        )
        env["WORKSPACE"] = os.path.join(os.path.dirname(intl),
                                        "workspace")
        env["DFL_ROOT"] = os.path.join(intl, "DeepFaceLab")
        env["TF_MIN_REQ_CAP"] = 30

        # collect _morePaths
        env["PATH"] = os.pathsep.join(
            self._morePaths + [os.environ["PATH"]]
        )
        self._chars = ""


    def train(self, model, baseModel="SAEHD", gpu="0"):
        """
        Run DFL_ROOT\main.py to train the model on the aligned data.
        (Mimic "6) train SAEHD.bat")

        Sequential arguments:
        model -- Name the model you want to create or reuse (to avoid
                 distorting the source incorrectly, the forum says to
                 use a model that uses the same source).
        baseModel -- Choose a base model that exists in a clean copy
                     of DeepFace Lab, such as "SAEHD" or "Quick96" which
                     will serve as a basis for creating a trained model
                     (used as the --model param for main.py, but does
                     not actually name the trained model--to name that,
                     use the model param of this method).
        gpu -- GPU number or comma-separated list of GPUs.
        """

        # "%PYTHON_EXECUTABLE%" "%DFL_ROOT%\main.py" train ^
        # --training-data-src-dir "%WORKSPACE%\data_src\aligned" ^
        # --training-data-dst-dir "%WORKSPACE%\data_dst\aligned" ^
        # --pretraining-data-dir "%INTERNAL%\pretrain_CelebA" ^
        # --model-dir "%WORKSPACE%\model" ^
        # --model SAEHD
        self._model = model
        self._gpu = gpu
        env = self.env
        ws = env["WORKSPACE"]
        intl = env["INTERNAL"]
        main_py = os.path.join(env["DFL_ROOT"], "main.py")
        if not os.path.isfile(main_py):
            raise RuntimeError("{} does not exist.".format(main_py))
        parts = [env["PYTHON_EXECUTABLE"], main_py, "train",
                 "--training-data-src-dir",
                 os.path.join(ws, "data_src", "aligned"),
                 "--training-data-dst-dir",
                 os.path.join(ws, "data_dst", "aligned"),
                 "--pretraining-data-dir",
                 os.path.join(intl, "pretrain_CelebA"),
                 "--model-dir",
                 os.path.join(ws, "model"),
                 "--model", baseModel]
        self.run_command(parts, shell=True)


    def monitor_output(self, out, isStdErr):
        """
        Monitor and handle the output of a stream.
        """
        while True:
            if self._p is None:
                break
            rawOut = out.read(1)
            self.handle_byte(rawOut, isStdErr)
            # self._q.put(line)
            if len(rawOut) < 1:
                break


        """
        for line in iter(out.readline, b''):
            # self._q.put(line)
            self.handle_bytes(line, isStdErr)
        """
        # ^ readline doesn't get partial lines such as prompts.
        print("Output finished (error stream: {})"
              "".format(isStdErr))
        out.close()


    def is_prompt(self, line):
        if line in self.prompts:
            return True
        for end in self.promptEnds:
            if line.endswith(end):
                return True
        return False


    def handle_byte(self, rawOut, isStdError):
        thisC = rawOut.decode(errors='ignore')
        self._chars += thisC
        # NOTE: rawOut may be b'\r' then later b'\n'
        # print('got "{}"'.format(rawOut))
        # print('got "{}"'.format(thisC))
        _chars = self._chars
        if _chars.endswith(os.linesep) or self.is_prompt(_chars):
            self._chars = ""  # prevent other thread from getting it!
            self.handle_line(_chars.rstrip(os.linesep), isStdError)
        else:
            pass
            # print("[dfl.py] waiting for more (have \"{}\")"
            # "".format(self._chars))


    def handle_bytes(self, rawOut, isStdError):
        line = rawOut.strip().decode(errors='ignore')
        self.handle_line(line, isStdError)

    def _enter_cmd(self, sendS, addNewline=True, silent=False):
        if not silent:
            print("[dfl.py] automatically entering: {}".format(sendS))
        # self._p.communicate(thisB)
        # ^ waits until process is terminated!
        if len(sendS) > 0:
            thisB = bytes(sendS, 'ascii')
            self._p.stdin.write(thisB)
        if addNewline:
            thisB = bytes(os.linesep, 'ascii')
            self._p.stdin.write(thisB)
        self._p.stdin.flush()
        # print("[dfl.py] entered: {}".format(sendS))


    def handle_line(self, line, isStdError):
        if len(line) < 1:
            # print()
            return
        print(line)
        if self._cmdDone:
            self._enter_cmd("", silent=True)  # press to continue
        for deadFlag in self.deadFlags:
            if deadFlag in line:
                self._cmdDone = True
                print("[dfl.py] detected a fatal error")
                self._enter_cmd("", silent=True)  # press to continue
                return
        parts = line.split(" : ")
        if self.is_prompt(line):
            handled = False
            if self._mode is None:
                raise RuntimeError("[dfl.py] could not detect mode"
                                   " (question) before prompt")
            # elif self._mode == "choose model":
            # print("[dfl.py] answering question...")
            if self._pressChar is None:
                if len(self._choices.keys()) > 0:
                    # There are already models, but there
                    # is no model chosen, so make one
                    if self._choseName is None:
                        raise ValueError("The script is"
                                         " asking for a"
                                         " name"
                                         " but you provided"
                                         " no existing or"
                                         " new name.")
                    print("[dfl.py] INFO: using \"{}\""
                          " and ignoring existing choices: {}"
                          "".format(self._choseName,
                                    self._choices.values()))
                else:
                    print("[dfl.py] INFO: using '{}'"
                          "".format(self._choseName))
                # print("[dfl.py] trying to type model")
                sendS = self._choseName
                self._enter_cmd(sendS)
                # print("[dfl.py] tried to type model")
            else:
                # print("[dfl.py] trying to press {}"
                # "".format(self._pressChar))
                sendS = self._pressChar
                self._enter_cmd(sendS)
                # print("[dfl.py] tried to press {}"
                # "".format(self._pressChar))
                self._pressChar = None
                self._mode = None
                self._choices = None
                self._commands = None
        elif self.any_in(self._continuePrompts, line):
            self._enter_cmd("")
            print("[dfl.py] tried to continue (entered newline)")
            # See <https://stackoverflow.com/questions/17173946/
            # python-batch-use-python-to-press-any-key-to-
            # continue>
        elif "saved model" in line:
            if self._mode is not None:
                raise RuntimeError('[dfl.py] found "saved model"'
                                   ' prompt before answering previous'
                                   ' question')
            # "Choose one of saved models, or enter a name to
            # create a new model." [sic]
            self._choices = {}
            self._commands = {}
            self._defaultName = None
            self._defaultChar = None
            self._mode = "choose model"
            self._pressChar = None
            self._choseName = self._model
            print("[dfl.py] detected question: {}".format(self._mode))
        elif "Choose one or several GPU idxs" in line:
            if self._mode is not None:
                raise RuntimeError('[dfl.py] found "saved model"'
                                   ' prompt before answering previous'
                                   ' question')
            # "Choose one or several GPU idxs (separated by comma)"
            self._choices = {}
            self._commands = {}
            self._defaultName = None
            self._defaultChar = None
            self._mode = "choose gpu"
            self._pressChar = self._gpu  # csv is ok
            self._choseName = None
        elif len(parts) == 2:
            parts[0] = parts[0].strip()
            if parts[0].startswith("[") and parts[0].endswith("]"):
                cmdChar = parts[0][1:-1]
                if (len(cmdChar) == 1) and (cmdChar in digits):
                    if self._mode == "choose model":
                        defFlag = " - latest"
                        if parts[1].endswith(defFlag):
                            parts[1] = parts[1][:-len(defFlag)]
                            self._defaultName = parts[1].strip()
                            self._defaultChar = cmdChar
                            # if self._mode == "choose model":
                            if self._model is None:
                                self._model = self._defaultName
                                self._pressChar = cmdChar
                    if parts[1] == self._choseName:
                        print("[dfl.py] INFO: Your"
                              " chosen model \"{}\" is"
                              " option {}"
                              "".format(self._choseName, cmdChar))
                        if self._pressChar is not None:
                            n0 = self._choseName
                            c1 = cmdChar
                            c0 = self._pressChar
                            raise ValueError('You wanted {} which is'
                                             'option {}, but already'
                                             'specified option {}'
                                             ''.format(n0, c1, c0))
                        self._pressChar = cmdChar

                    self._choices[cmdChar] = parts[1].strip()
                else:
                    self._commands[cmdChar] = parts[1].strip()
            else:
                print('[dfl.py] ^ unrecognized option format'
                      ' (expected "[x] : Description" where x is a'
                      ' letter or number)')
        else:
            pass
            # print("[dfl.py] ^ unrecognized line")

    def run_command(self, parts, shell=False):
        """
        Run a DeepFace Lab console script and capture the output.
        """
        if self._runCmd is not None:
            raise RuntimeError("There is already a command running.")
        self._cmdDone = False
        cmd = parts[0]
        self._runCmd = parts
        for i in range(1, len(parts)):
            part = parts[i]
            if " " in part:
                cmd += '" {}"'.format(part)
            else:
                cmd += ' {}'.format(part)
        print("[dfl.py] Running {}...".format(cmd))

        devnull = None
        try:
            devnull = subprocess.DEVNULL
        except AttributeError:
            # Python2
            devnull = open(os.devnull,'r')
            # as per  Brent Writes Code Feb 29 '16 at 21:07
            # (comment to Bryce Guinta's Jan 12 '16 at 17:26 answer)
            # on <https://stackoverflow.com/questions/11729562/
            # disable-pause-in-windows-bat-script>
        # NOTE: Calling Popen with stdin=devnull
        # prevents pause, but there are other questions other than
        # "press any key to continue" to answer so that is not
        # applicable.

        # Python 3.5 adds low-level function subprocess.run
        # which also accepts same params as above plus others:
        # https://docs.python.org/3/library/subprocess.html
        print("[dfl.py] Opening process...")
        self._p = subprocess.Popen(parts, env=self.getenv(),
                                   cwd=self.env["~dp0"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   shell=shell, close_fds=True)
        # close_fds: Do not let the subproces inherit open file
        # descriptors.
        self._code = None
        self._mode = None
        self._choices = None
        self._commands = None
        self._defaultName = None
        # ^ default Name to help choose defaultChar
        # ^ that is the value after the command, such as rename in:
        # [r] : rename
        #  where 'r' is cmdChar (pressChar is a cmdChar to send stdin)
        self._defaultChar = None  # default value for pressChar
        self._pressChar = None  # send this character to stdin
        # self._q = Queue()
        self._t0 = None
        self._t1 = None
        self._t0 = Thread(target=self.monitor_output,
                          args=(self._p.stdout, False))
        self._t0.daemon = True # thread dies with the program
        self._t0.start()
        self._t1 = Thread(target=self.monitor_output,
                          args=(self._p.stderr, True))
        self._t1.daemon = True # thread dies with the program
        self._t1.start()

        while True:
            # print("[dfl.py] Polling...")
            self._code = self._p.poll()
            if self._code is not None:
                print("[dfl.py] The process completed with exit code {}"
                      "".format(code))
                break
            if self._cmdDone:
                print("[dfl.py] terminating watch threads...")
                self._t0.join()
                self._t0 = None
                self._t1.join()
                self._t1 = None
                if self._p is not None:
                    print("[dfl.py] terminating process...")
                    self._p.terminate()
                    self._p = None
                break
            """
            stdout, stderr = self._p.communicate()
            print("[dfl.py] Reading output stream...")
            se = ''
            so = self._p.stdout.readline()
            so = nonBlockReadline(self._p.stdout)

            if getErr:
                print("[dfl.py] Reading error stream...")
                se = self._p.stderr.readline()
                ^ will wait forever
                se = nonBlockReadline(self._p.stderr)

            so, se = (self._p.stdout.readline(),
                      self._p.stderr.readline())
            stdall = [so, se]
            """
        self._p = None
        self._cmdDone = True
        self._runCmd = None
        return self._code


    def getenv(self):
        ret = os.environ.copy()
        for k, v in self.env.items():
            if k == "~dp0":
                pass
                # os.chdir(v)
            elif v is None:
                pass
                # os.environ.remove(k)
            elif k == "PATH":
                # Make sure it is up to date:
                # os.environ["PATH"] = os.pathsep.join(
                # self._morePaths + [os.environ["PATH"]]
                # )
                ret[k] = str(v)
            else:
                ret[k] = str(v)
        return ret


    def setenv(self):
        # Usually, use subprocess.Popen(path, env=self.env) instead
        # (wipe vars with None in a copy though)
        for k, v in self.env.items():
            if k == "~dp0":
                os.chdir(v)
            elif v is None:
                os.environ.remove(k)
            elif k == "PATH":
                # Make sure it is up to date:
                os.environ["PATH"] = os.pathsep.join(
                    self._morePaths + [os.environ["PATH"]]
                )
            else:
                os.environ[k] = str(v)


    def help():
        return dfl_help_fmt.format(dflDir)


    def help_install():
        return dfl_install_help_fmt.format(dflDir)

    def choose_param(name, videoPath):
        if videoPath is None:
            raise ValueError("videoPath was None in DFL choose_param.")
        dfSource = os.path.join(self.env["WORKSPACE"], "data_src.mp4")
        dfDest = os.path.join(self.env["WORKSPACE"], "data_dst.mp4")
        copyAs = None
        if name == "destination":
            copyAs = dfDest
        elif name == "source":
            copyAs = dfSource
        else:
            raise ValueError("{} is an unknown DeepFace Lab Param--choose"
                               ": {}".format(name, dfl_params.keys()))
        if os.path.isfile(copyAs):
            os.remove(copyAs)
        shutil.copy(videoPath, copyAs)
        videoName = os.path.split(videoPath)[1]
        print("[dfl.py] * wrote {} to {}.".format(videoName, copyAs))


    def choose_param_in(name, video_dir):
        if not os.path.isdir(self.env["WORKSPACE"]):
            print()
            print(self.help())
            print()
            raise RuntimeError("DeepFace Lab doesn't exist here: {}"
                               "".format(self.env["WORKSPACE"]))
        videoPath = None
        paths = []
        for sub in os.listdir(video_dir):
            subPath = os.path.join(video_dir, sub)
            if not subPath.lower().endswith(".mp4"):
                continue
            videoPath = subPath
            break
        if videoPath is None:
            raise ValueError("There was no .mp4 to select in {}"
                             "".format(video_dir))
        self.choose_param(name, videoPath)
