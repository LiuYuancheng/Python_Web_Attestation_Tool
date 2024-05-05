#-----------------------------------------------------------------------------
# Name:        PhishperidaPKG.py
#
# Purpose:     This module is used to package the NUS-Phishperida phishing url 
#              detection project as a black box API for other project to use. 
#              put this module in the same folder of the NUS-Phishperida's 'main'
#              module.
#              NUS-Phishperida link: https://github.com/lindsey98/Phishpedia
# 
# Author:      
#
# Created:     2020/11/24
# Version:     v_0.1
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
from phishpedia_config import *
from src.util.chrome import *
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
print("Current working directory is : %s" % os.getcwd())
DRI_PATH = os.path.dirname(__file__)

# defined the used file name.
RST_FILE = 'pedia_rlt.txt' # result recode file.
URL_FILE= 'info.txt' # url file name
OUT_FILE = "shot.png"
PREDIC_FILE = "predict.png"

#####################################################################################################################
# ** Step 1: Enter Layout detector, get predicted elements
# ** Step 2: Enter Siamese, siamese match a phishing target, get phishing target

# **         If Siamese report no target, Return Benign, None
# **         Else Siamese report a target, Return Phish, phishing target
#####################################################################################################################

def mainRun(url, screenshot_path):
    '''
    Phishdiscovery for phishpedia main script
    :param url: URL
    :param screenshot_path: path to screenshot
    :return phish_category: 0 for benign 1 for phish
    :return pred_target: None or phishing target
    :return plotvis: predicted image
    :return siamese_conf: siamese matching confidence
    '''

    # 0 for benign, 1 for phish, default is benign
    phish_category = 0
    pred_target = None
    siamese_conf = None
    print("Entering phishpedia")

    ####################### Step1: layout detector ##############################################
    pred_boxes, _, _, _ = pred_rcnn(im=screenshot_path, predictor=ele_model)
    pred_boxes = pred_boxes.detach().cpu().numpy()  # get predicted logo box
    plotvis = vis(screenshot_path, pred_boxes)
    print("plot")

    # If no element is reported
    if len(pred_boxes) == 0:
        print('No element is detected, report as benign')
        return phish_category, pred_target, plotvis, siamese_conf
    print('Entering siamese')

    ######################## Step2: Siamese (logo matcher) ########################################
    pred_target, matched_coord, siamese_conf = phishpedia_classifier_logo(logo_boxes=pred_boxes,
                                                                          domain_map_path=domain_map_path,
                                                                          model=pedia_model,
                                                                          logo_feat_list=logo_feat_list,
                                                                          file_name_list=file_name_list,
                                                                          url=url,
                                                                          shot_path=screenshot_path,
                                                                          ts=siamese_ts)

    if pred_target is None:
        print('Did not match to any brand, report as benign')
        return phish_category, pred_target, plotvis, siamese_conf

    else:
        phish_category = 1
        # Visualize, add annotations
        cv2.putText(plotvis, "Target: {} with confidence {:.4f}".format(pred_target, siamese_conf),
                    (int(matched_coord[0] + 20), int(matched_coord[1] + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    return phish_category, pred_target, plotvis, siamese_conf


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class phishperidaPKG(object):

    def __init__(self):
        """ Init the object and create the result record file.
        """
        self.resultsPath = os.path.join(DRI_PATH, RST_FILE)
        if not os.path.exists(self.resultsPath):
            titleArr = ('folder', 'url', 'phish', 'prediction', 'siamese_conf', 'vt_result', 'runtime')
            with open(self.resultsPath, "w+") as f:
                f.write("\t".join(titleArr)+"\n")
   
   #-----------------------------------------------------------------------------
    def phishperidaCheck(self, directory):        
        for item in tqdm(os.listdir(directory)):
            start_time = time.time()
            try:
                print(item)
                full_path = os.path.join(directory, item)
                screenshot_path = os.path.join(full_path, OUT_FILE)
                url = open(os.path.join(full_path, URL_FILE), encoding='ISO-8859-1').read()
                if not os.path.exists(screenshot_path):
                    continue
                else:
                    phish_category, phish_target, plotvis, siamese_conf = mainRun(url=url, screenshot_path=screenshot_path)
                    # FIXME: call VTScan only when phishpedia report it as phishing
                    vt_result = "None"
                    if phish_target is not None:
                        try:
                            if vt_scan(url) is not None:
                                positive, total = vt_scan(url)
                                print("Positive VT scan!")
                                vt_result = str(positive) + "/" + str(total)
                            else:
                                print("Negative VT scan!")
                                vt_result = "None"
                        except Exception as e:
                            print('VTScan is not working...')
                            vt_result = "error"
                    # write results as well as predicted images
                    with open(self.resultsPath, "a+", encoding='ISO-8859-1') as f:
                        f.write('\t'.join((item, url, str(phish_category), str(phish_target), str(
                            siamese_conf), vt_result, str(round(time.time() - start_time, 4))))+'\n')
                        # f.write(item + "\t")
                        # f.write(url + "\t")
                        # f.write(str(phish_category) + "\t")
                        # f.write(str(phish_target) + "\t")  # write top1 prediction only
                        # f.write(str(siamese_conf) + "\t")
                        # f.write(vt_result + "\t")
                        # f.write(str(round(time.time() - start_time, 4)) + "\n")
                    cv2.imwrite(os.path.join(full_path, PREDIC_FILE), plotvis)
            except Exception as e:
                print(str(e))

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    checker = phishperidaPKG()
    checker.phishperidaCheck('./datasets/test_sites')
