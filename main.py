from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from math import pi, sin, cos


class Container(BoxLayout):
    orientation = 'vertical'
    counted = False
    containsDot = False
    brackets = 0
    mode = 0
    modes = ['rad', 'deg']

    def deg_to_rad(self, grad):
        return grad / 360 * pi * 2

    def mycos(self, grad):
        return cos(self.deg_to_rad(grad))

    def mysin(self, grad):
        return sin(self.deg_to_rad(grad))

    def rad_pressed(self, instance):
        if instance.text == 'rad':
            self.mode = 1
            instance.text = self.modes[1]
        else:
            self.mode = 0
            instance.text = self.modes[0]

    def clear(self, instance):
        self.resInp.text = ''
        self.counted = False
        self.containsDot = False
        self.brackets = 0

    def sin_pressed(self, txt):
        if self.counted:
            self.resInp.text = ''
            self.counted = False
        if self.resInp.text != '' and self.resInp.text[-1] not in '%/*+-(':
            self.resInp.text += '*'
        self.resInp.text += txt + '('
        self.brackets += 1

    def count(self, formula):
        while self.brackets > 0:
            formula += ')'
            self.brackets -= 1
        self.counted = True
        self.containsDot = False
        try:
            self.resInp.text = formula + "="
            if self.mode:
                formula = formula.replace('sin', 'self.mysin', len(formula))
                formula = formula.replace('cos', 'self.mycos', len(formula))
            self.resInp.text += str(eval(formula))

        except Exception as e:
            print(e)
            self.resInp.text += '\nОшибка'
            print(formula)
    def add_step(self, instance):
        if self.resInp.text == '' or self.counted or self.resInp.text[-1] == '.':
            return
        elif self.resInp.text[-1] in '%*/-+(.':
            if self.resInp.text[-1] == '(':
                if instance.text == '-':
                    self.resInp.text += instance.text
                else:
                    return
            else:
                self.resInp.text = self.resInp.text[:-1] + instance.text
        else:
            self.containsDot = False
            self.resInp.text += instance.text

    def pressed(self, instance):
        if self.counted:
            self.resInp.text = ''
        if instance.text in ')' and (self.resInp.text == '' or self.resInp.text[-1] in '-+*/%.'):
            return
        if self.resInp.text != '' and self.resInp.text[-1] == '(' and instance.text == ')':
            return
        if self.counted:
            self.counted = False
            self.resInp.text = ''
        if (self.resInp.text != '') and ((self.resInp.text[-1] in "0123456789)i") and (instance.text in '(pi')):
            self.resInp.text += '*'
        if (self.resInp.text!='') and(self.resInp.text[-1] in 'i') and(instance.text in '01234567890'):
            self.resInp.text+= '*'
        if self.resInp.text != '' and self.resInp.text[-1] in '0123456789i' and instance.text in 'pi(':
            self.resInp.text += '*'
        if instance.text == ')' and not self.brackets:
            return
        self.resInp.text += instance.text
        if instance.text == '(':
            self.brackets += 1
        elif instance.text == ')':
            self.brackets -= 1

    def dot_pressed(self, instance):
        if self.resInp.text[-1] in '0123456789' and not self.containsDot:
            self.containsDot = True
            self.resInp.text += '.'


class mainApp(App):
    def build(self):
        return Container()


if __name__ in ('__main__', '__android__'):
    app = mainApp()
    app.run()

