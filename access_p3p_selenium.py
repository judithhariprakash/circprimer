from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

def scrap_p3p(sequence, target):
    result = {}
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Firefox()
        try: 
            driver.get("http://www.bioinformatics.nl/cgi-bin/primer3plus/primer3plus.cgi")
            elem_seq = driver.find_element_by_name("SEQUENCE")
            elem_seq.send_keys(sequence)
            elem_seq = driver.find_element_by_name("TARGET")
            elem_seq.send_keys(target)
            elem_pp = driver.find_element_by_name("Pick_Primers")
            elem_pp.send_keys(Keys.RETURN)
            
            for num, i in enumerate(range(0,10,2)):
                elem_f = driver.find_element_by_name("PRIMER_%d_SEQUENCE" % i)
                j=i+1
                elem_r = driver.find_element_by_name("PRIMER_%d_SEQUENCE" % j)
                m=num+1
                result['primer_set_%d' % m] = {'forward_sequence': str(elem_f.get_attribute("value")),
                                               'reverse_sequence': str(elem_r.get_attribute("value"))}
            
            ctr=1
            x = 'f'
            all_options = driver.find_elements_by_xpath("//td")
            for option in all_options:
                t = unicode(option.text)
                if len(t) > 0:
                    if t[:5] == "Start":
                        if x == 'f':
                            result['primer_set_%d' % ctr]['forward_start_pos'] = t[6:].lstrip(' ')
                        else:
                            result['primer_set_%d' % ctr]['reverse_start_pos'] = t[6:].lstrip(' ')
                    if t[:6] == "Length":
                        if x  == 'f':
                            result['primer_set_%d' % ctr]['forward_length'] = t[7:].lstrip(' ')
                        else:
                            result['primer_set_%d' % ctr]['reverse_length'] = t[7:].lstrip(' ')
                    if t[:2] == "Tm":
                        if x  == 'f':
                            result['primer_set_%d' % ctr]['forward_tm'] = t[3:].lstrip(' ')
                            x = 'r'
                        else:
                            result['primer_set_%d' % ctr]['reverse_tm'] = t[3:].lstrip(' ')
                    if t[:12] == "Product Size":
                        result['primer_set_%d' % ctr]['product_size'] = t[13:].lstrip(' ')
                        ctr+=1
        finally:
            driver.close()
    finally:
        display.stop()
    
    return result
