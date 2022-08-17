"""Supervisor of the Robot Programming benchmark."""

from controller import Supervisor
import os
import sys

def benchmarkPerformance(message, robot):
    benchmark_name = message.split(':')[1]
    benchmark_performance_string = message.split(':')[3]
    print(benchmark_name + ' Benchmark complete! Your performance was ' + benchmark_performance_string)
    if robot.getFromDef("ANIMATION_RECORDER_SUPERVISOR"):
        stop_recording(robot, message)

def stop_recording(robot, message):
    emitter = robot.getDevice('emitter')
    emitter.send(message.encode('utf-8'))

""" try:
    includePath = "../../../include"
    includePath.replace('/', os.sep)
    sys.path.append(includePath)
    from benchmark import benchmarkPerformance
except ImportError:
    print("error")
    sys.stderr.write("Warning: 'benchmark' module not found.\n")
    sys.exit(0) """

robot = Supervisor()

timestep = int(robot.getBasicTimeStep())

thymio = robot.getFromDef("BENCHMARK_ROBOT")
translation = thymio.getField("translation")

tx = 0
running = True
while robot.step(timestep) != -1:
    t = translation.getSFVec3f()
    if running:
        percent = 1 - abs(0.25 + t[0]) / 0.25
        if percent < 0:
            percent = 0
        if t[0] < -0.01 and abs(t[0] - tx) < 0.0001:  # away from starting position and not moving any more
            running = False
            name = 'Robot Programming'
            performance = str(percent)
            performanceString = str(round(percent * 100, 2)) + '%'
            message = 'success:' + name + ':' + performance + ':' + performanceString
            robot.wwiSendText(message)
            benchmarkPerformance(message, robot)
        else:
            message = "percent"
        message += ":" + str(percent)
        robot.wwiSendText(message)
        tx = t[0]
    else:  # wait for record message
        message = robot.wwiReceiveText()
        while message:
            if message.startswith("confirm:"):
                print("WINDOW MESSAGE:", message)
            """ if message.startswith("success:"):
                benchmarkPerformance(message, robot)
                break """
            message = robot.wwiReceiveText()

robot.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
