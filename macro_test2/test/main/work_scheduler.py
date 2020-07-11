import pyautogui as pag


class work:
    def __init__(self):
        pass

    def start(self, aScheduler):

        for scd in aScheduler:
            action = scd.get('action')
            value = scd.get('obj')
            position = ''
            res = 0

            if action == 'POS':
                pag.moveTo(value)
            elif action == 'CLICK':
                pag.click()
            elif action == 'KEYWORD':
                pag.typewrite(value)
            else:
                print('[W01] ERROR UNKNOWN ACTION')
                res = -1

        return res

    def set_scheduler(self):
        pass
    def del_scheduler(self):
        pass