import math
from random import gauss, sample
import json

pi = math.pi

def metric(phi, phi2, phi_res, dist, dist2, dist_res):
    # function calculates the distance between two sample points
    # phi .... reference angle measurement for robustness
    # phi2 .... second angle measurement
    # phi_res .... resolution of angle measurement sensor
    # dist .... reference distance measurement for robustness
    # dist2 .... second distance measurement
    # dist_res .... distance resolution of sensor
    # returns metric value:
    # metric<2 .... measurement2 inside robustness set of reference measurment 
    # metric>2 .... measurement2 outside robustness set of reference measruement

    # to calcluate the treshold value the following assumption are used
    # as base use a multiple of the sensor resolution 2*phi_res
    multiple = 2
    # increase it to ensure overlapping by xx percentage 1.05
    tresh = 1.05
    phi_tresh = tresh*multiple*phi_res 
    phi_metric = abs(phi-phi2)/phi_tresh # norm angle
    dist_tresh = tresh*multiple*dist_res 
    dist_metric = abs(dist-dist2)/dist_tresh # norm angle
    metric = phi_metric + dist_metric
    return metric

def main ():
    print('Generating measurements for Spiki robustness demonstration')
    # sensor specification
    dist_min = 5
    dist_max = 100
    dist_res = 40#10
    dist_sig = 0.1
    phi_min = -30*pi/180
    phi_max = 30*pi/180
    phi_res = 15*pi/180#5*pi/180
    phi_sig = 0.1*pi/180
    
    # object specification
    # width of objects
    # TODO include it into code to further limit the useable measurement range
    d_obj_min = 0.2
    d_obj_max = 0.4

    # useable sensor spec
    # describes the set where sensor measurements are typically useable
    dist_min_usable = 30
    dist_max_usable = 70
    phi_min_usable = -20*pi/180
    phi_max_usable = 20*pi/180

    phi = phi_min
    object_list = []
    dist_usable = dist_max_usable-dist_min_usable
    # dist_list = [dist_min_usable +dist_usable/4+ i*dist_usable/2 for i in range(-1,3)]
    dist_list = [dist_min_usable + dist_usable/2 + i*dist_usable for i in range(-1,2)]
    phi_usable = phi_max_usable - phi_min_usable
    # phi_list = [phi_min_usable +phi_usable/4+ i*phi_usable/2 for i in range(-1,3)]
    phi_list = [phi_min_usable + phi_usable/2 + i*phi_usable for i in range(-1,2)]
    for dist in dist_list:
        for phi in phi_list:
            object = {}
            object['dist'] = dist
            object['dist_meas'] = gauss(dist,dist_sig)
            object['phi'] = phi
            object['phi_meas'] = gauss(phi,phi_sig)
            object_list.append(object)
    # while (phi<phi_max):
    #     # print(phi)
    #     # sweep through angle measurement
    #     dist = dist_min
    #     while (dist<dist_max):
    #         # print(dist)
    #         # sweep through distance measurement
    #         object = {}
    #         # object['dist'] = 0
    #         object['dist'] = dist
    #         # object['dist_meas'] = 0
    #         object['dist_meas'] = gauss(dist,dist_sig)
    #         object['phi'] = phi
    #         object['phi_meas'] = gauss(phi,phi_sig)
    #         #print(str(object))
    #         # if phi>=phi_min_usable and phi<=phi_max_usable and dist>=dist_min_usable and dist<=dist_max_usable:
    #         #     # object inside usable measurement range
    #         #     object['dist'] = dist
    #         #     object['dist_meas'] = gauss(dist,dist_sig)
    #         object_list.append(object)
    #         #print(str(dist) + ' ' + str(dist_min_usable) + ' ' + str(phi) + ' ' + str(phi_min_usable))
    #         #print(str(object))
    #         dist = dist + dist_res  
    #     phi = phi + phi_res
    # # print(object_list)
    print(object_list)

    # incomplete_measurements = sample(object_list,int(len(object_list)*0.3))
    sensor_specs = {
    'dist_min': dist_min,
    'dist_max': dist_max,
    'dist_res': dist_res,
    'dist_sig': dist_sig,
    'phi_min': -30 * math.pi / 180,
    'phi_max': 30 * math.pi / 180,
    'phi_res': phi_res,
    'phi_sig': 0.1 * math.pi / 180
    }
    specification_space = {
    'dist_min_usable': 20,
    'dist_max_usable': 70,
    'phi_min_usable': -20 * math.pi / 180,
    'phi_max_usable': 20 * math.pi / 180
    }
    

    with open('sensor_specifications', 'w') as file:
        json.dump(sensor_specs, file, indent=4)

    with open('specification_space', 'w') as file:
        json.dump(specification_space, file, indent=4)  

    with open(r'C:\Users\Enrico Del Re\Documents\Spiki\Training-robust-neural-networks-using-Lipschitz-bounds\measurements.meas', 'w') as f:
        print("dumping")
        json.dump(object_list, f, indent=4)

    # with open('incomplete_data.json', 'w') as f:
    #     print("dumping")
    #     json.dump(incomplete_measurements, f, indent=4)
 
if __name__ == '__main__':
    main()