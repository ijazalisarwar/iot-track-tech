import logging, json
import azure.functions as func
import numpy as np
from scipy.signal import find_peaks,peak_prominences,savgol_filter


def main(msg: func.ServiceBusMessage,  outdoc: func.Out[func.Document]):
    try:
        result = json.loads(msg.get_body().decode("utf-8"))
        coordinates=result['ycoord_list']
        time_list=result['time_list']

        #Perform data analysis
        repetitionNumber,filtered_coord=dataanalysis(time_list,coordinates)

        #Output dictionary
        output_dict={'Repetitions':repetitionNumber, 'Coordinates':filtered_coord}
        outdoc.set(func.Document.from_dict(output_dict))

    except Exception as ex:
        logging.info('Exception because of: %s', str(ex))

def dataanalysis(time,coordinates):

    time=np.array(time)
    coordinates=np.array(coordinates)
    

    #Remove bad datapoints
    remove_bad_points_mask=np.where(coordinates==0.0)

    coordinates=np.delete(coordinates,remove_bad_points_mask)

    #Normalize data
    coordinates=((coordinates-np.min(coordinates))/(np.max(coordinates)-np.min(coordinates)))

    #Perform Savitzky–Golay filter
    filtered_coord=savgol_filter(coordinates,window_length=25,polyorder=2)
    filtered_coord=((filtered_coord-np.min(filtered_coord))/(np.max(filtered_coord)-np.min(filtered_coord)))

    #Reverse y-axis, so it corresponds to true coordinate system
    filtered_coord=(filtered_coord-1)*(-1)

    #Number of repetitions:
    peak_max, _ = find_peaks(filtered_coord, prominence=0.5)
    repetition_number = len(peak_max)

    filtered_coord=filtered_coord.tolist()

    return repetition_number,filtered_coord



