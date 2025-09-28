import sys
sys.path.append('/home/veins/src/sumo/tools')

import traci
import math
import time

PORT = 8813


MAX_SPEED = 50.0
MAX_SPEED_DELTA = 15.0
MAX_POSITION_JUMP = 50.0
POSITION_TOLERANCE = 3.0


last_positions = {}
last_speeds = {}

def distance(p1, p2):
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def detect_misbehavior(step):
	global last_positions, last_speeds

	vehicle_ids = traci.vehicle.getIDList()
	current_positions = {}
	current_speeds = {}

	for vid in vehicle_ids:
		pos = traci.vehicle.getPosition(vid)
		speed = traci.vehicle.getSpeed(vid)
		current_positions[vid] = pos
		current_speeds[vid] = speed
	
	for vid in vehicle_ids:
		pos = current_positions[vid]
		speed = current_speeds [vid]
		
		if speed > MAX_SPEED:
			print(f"[{step}] High Speed: {vid} speed={speed:.1f} m/s")

		if vid in last_speeds:
			delta_speed = abs(speed - last_speeds[vid])
			if delta_speed > MAX_SPEED_DELTA:
				print(f"[{step}] Speed Jump: {vid} deltav={delta_speed:.1f} m/s")

		if vid in last_positions:
			dist = distance(pos, last_positions[vid])
			if dist > MAX_POSITION_JUMP:
				print(f"[{step}] Position jump: {vid} moved {dist:.1f} m in one step")

		try:
			lane_id = traci.vehicle.getLaneID(vid)
			if lane_id == "":
				print(f"[{step}] Possible ghost vehicle: {vid} has no lane assignment")
		except traci.TraCIException:
			print(f"[{step}] Possible ghost vehicle: {vid} not found in lane data")


	ids = list(current_positions.keys())
	for i in range(len(ids)):
		for j in range(i+1, len(ids)):
			d = distance(current_positions[ids[i]], current_positions[ids[j]])
			if d < POSITION_TOLERANCE:
				print(f"[{step}] Possible sybil attack: {ids[i]} and {ids[j]} are {d:.1f} m apart")

	last_positions = current_positions
	last_speeds = current_speeds

def main():
	traci.init(PORT)
	traci.setOrder(1)
	print(" Connected to SUMO")
	
	try:
		while traci.simulation.getMinExpectedNumber() > 0:
			traci.simulationStep()
			step = traci.simulation.getTime()
			detect_misbehavior(step)
			time.sleep(0.005)
	except KeyboardInterrupt:
		print("Detection Stopped")
	finally:
		traci.close()

if __name__ == "__main__":
	main()
