import sys
sys.path.append('/home/veins/src/sumo/tools')

import traci
import math
import time

PORT = 8813
STEP = 0.1


def inject_position_spoof(vid, x, y):
	try:
		edge = traci.vehicle.getRoadID(vid)
		traci.vehicle.moveToXY(vid, edge, 0, x, y, keepRoute=0)
		print(f"[{traci.simulation.getTime():.1f}] Position spoof injected: {vid} -> ({x:.1f},{y:.1f})")
	except Exception as e:
		print(f"Position spoof failed: {e}")

def inject_sybil(base_x, base_y, count=3, prefix="sybil"):
	created = []
	for i in range(count):
		vid = f"{prefix}_{int(time.time()*1000)%100000}_{i}"
		try:
			traci.vehicle.add(vid, routeID="", typeID="vtype0")
			traci.vehicle.moveToXY(vehID=vid, edgeID="", lane=0, x=base_x, y=base_y, angle=0.0, keepRoute=2)
			
			if i == 0:
				traci.vehicle.setMaxSpeed(vid, 100.0)
				traci.vehicle.slowDown(vid, 80.0, 0)
			
			created.append(vid)
		except Exception as e:
			print(f"Sybil creatin failed for {vid}: {e}")
	print(f"{traci.simulation.getTime():.1f}] Sybil vehicles created: {created}")
	return created
	
def inject_ghost_vehicle(base_x=0.0, base_y=0.0, vid_prefix="ghost"):
	ghost_id = f"{vid_prefix}_{int(time.time()*1000) % 100000}"
	
	try:
		traci.vehicle.add(ghost_id, routeID="", typeID="vtype0")
		
		traci.vehicle.moveToXY(vehID=ghost_id, edgeID="", lane=0, x=base_x+1000.0, y=base_y+1000.0, angle=0.0, keepRoute=2)
		print(f"[{traci.simulation.getTime():.1f}] Ghost vehicle '{ghost_id}' created at ({base_x+1000.0}, {base_y + 1000.0})")
		return ghost_id
		
	except Exception as e:
		print(f" failed to create ghost vehicle: {e}")
		return None

def main():
	print("Connecting to SUMO...")

	traci.init(PORT)
	traci.setOrder(2)
	step = 0
	try:
		while traci.simulation.getMinExpectedNumber() > 0:
			traci.simulationStep()

			simtime = traci.simulation.getTime()
			vids = traci.vehicle.getIDList()

			if abs(simtime - 100.0) < 1e-6 and len(vids) > 1:
				x, y = traci.vehicle.getPosition(vids[1])
				inject_position_spoof(vids[1], x + 100, y + 100)

			if abs(simtime - 150.0) < 1e-6 and vids:
				x, y = traci.vehicle.getPosition(vids[0])
				inject_sybil(x, y, count=3)
				
			if abs(simtime - 200.0) < 1e-6:
				inject_ghost_vehicle(base_x=0.0, base_y=0.0)

			step += 1
	except KeyboardInterrupt:
		print("Stopping simulation...")
	finally:
		traci.close()

if __name__ == "__main__":
	main()
