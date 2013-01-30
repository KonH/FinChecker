# -*- coding: utf-8 -*-
# TODO:
# - Шифрование

filename = 'file.txt'

import aes
import pylab
import time
import random
import os
from datetime import datetime

# Direction of operation
class Direction:
    Input = 0
    Output = 1

    @staticmethod
    def get_value(value):
        assert type(value) == str
        if value == 'Input':
            return Direction.Input
        else:
            if value == 'Output':
                return Direction.Output
            else:
                return -1

    @staticmethod  
    def get_str(value):
        assert type(value) == int
        if value == Direction.Input:
            return 'Input'
        if value == Direction.Output:
            return 'Output'
        return 'Unknown'

# Operation
class Operation:
        
    def __init__(self, name, tags, value, direction, dt):
        assert type(name) == str
        assert type(tags) == list
        for tag in tags:
            assert type(tag) == str
        assert type(value) == float
        assert type(direction) == int
        assert type(dt) == datetime
        self.name = name
        self.tags = tags
        self.value = value
        self.direction = direction
        self.datetime = dt

    def __str__(self):
        result = ''
        result += 'Name: ' + self.name
        result += '\nTags: '
        for tag in self.tags:
            result += tag + '; '
        result += '\nValue: ' + str(self.value)
        result += '\nDirection: ' + Direction.get_str(self.direction)
        result += '\nDatetime: ' + str(self.datetime)
        return result

    def getShortInfo(self):
        result = ''
        if(self.direction == Direction.Input):
            result += '+'
        if(self.direction == Direction.Output):
            result += '-'
        result += str(self.value)
        result += '('
        for tag in self.tags:
            result += tag + ', '
        result += str(self.datetime) + ')'
        return result
    
    # Загрузка из строки сформированной __str__ класса
    @staticmethod
    def load(lines):
        sublines = []
        for line in lines:
            sublines.append(line.split(':'))
        name = ''
        tags = []
        value = 0.0
        direction = -1
        dt = datetime.today()
        for subline in sublines:
            if subline[0] == 'Name':
                name = subline[1][1:len(subline[1]) - 1] # Нужно обрезать первый пробел и перевод строки в конце
            if subline[0] == 'Tags':
                spaced_tags = subline[1].split(';')
                for i in range(0, len(spaced_tags) - 1):
                    tags.append(spaced_tags[i][1:])
            if subline[0] == 'Value':
                value = float(subline[1])
            if subline[0] == 'Direction':
                direction = Direction.get_value(subline[1][1:len(subline[1]) - 1])
            if subline[0] == 'Datetime':
                # Деление строки
                first_splitted = subline[1].split(' ')
                second_splitted = first_splitted[1].split('-')
                year = int(second_splitted[0])
                month = int(second_splitted[1])
                day = int(second_splitted[2])
                hour = int(first_splitted[2])
                minute = int(subline[2])
                dt = datetime(year, month, day, hour, minute)
        return Operation(name, tags, value, direction, dt)

# Main class
class FinChecker:

    def __init__(self):
        self.operations = []
        
    def addOperation(self, operation):
        assert isinstance(operation, Operation)
        self.operations.append(operation)

    # Get balance for date dt
    def getBalance(self, dt):
        assert type(dt) == datetime
        balance = 0.0
        for operation in self.operations:
            # Get operations earlier
            if operation.datetime <= dt:
                if operation.direction == Direction.Input:
                    balance += operation.value
                if operation.direction == Direction.Output:
                    balance -= operation.value
        return balance

    def getOperationsInfo(self):
        result = ''
        for op in self.operations:
            result += '\n' + str(op) + '\n'
        return result

    def getOperationsInfo_short(self):
        result = ''
        for op in self.operations:
            result += '\n' + op.getShortInfo() + '\n'
        return result

    def drawPlots(self, dt):
        self.drawPlotBalance(dt)
        self.drawPlotInput(dt)
        self.drawPlotOutput(dt)

    def drawPlotBalance(self, dt):
        i = 0
        x = []
        y = []
        for operation in self.operations:
            x.append(i)
            i += 1
            y.append(self.getBalance(operation.datetime))
        pylab.plot(x, y)
        pylab.title('Balance plot') 
        pylab.show()
        
    def drawPlotInput(self, dt):
        i = 0
        x = []
        y = []
        for operation in self.operations:
            x.append(i)
            i += 1
            if operation.datetime <= dt:
                if operation.direction == Direction.Input:
                    y.append(operation.value)
                else:
                    y.append(0.0)
        pylab.plot(x, y)
        pylab.title('Input')
        pylab.show()
        
    def drawPlotOutput(self, dt):
        i = 0
        x = []
        y = []
        for operation in self.operations:
            x.append(i)
            i += 1
            if operation.datetime <= dt:
                if operation.direction == Direction.Output:
                    y.append(operation.value)
                else:
                    y.append(0.0)
        pylab.plot(x, y)
        pylab.title('Output')
        pylab.show()

    def save(self, filename):
        assert type(filename) == str
        ser_str = ''
        for op in self.operations:
            ser_str += str(op) + '\n\n'
        f = open(filename, 'w')
        f.write(ser_str)
        f.close()

    def load(self, filename):
        assert type(filename) == str
        f = open(filename)
        lines = f.readlines()
        for i in range(0, len(lines), 6):
            op = Operation.load(lines[i : i + 5])
            self.operations.append(op)

print 'Welcome to FinanceChecker 0.3!'

f = FinChecker()

if(os.path.exists(filename)):
    # Вариант повторного запуска
    print 'Welcome back!'
    f.load(filename)
else:
    # Вариант первого запуска
    print 'This is first launch!'
    print '(you need to set filename in script header, by default is is \'file.txt\', now it is \'' + filename + '\')'

# Меню
choose = -1
while(True):
    print 'Your current balance is ' + str(f.getBalance(datetime.today()))
    print '1) Add operation'
    print '2) Show operations (20 for short version)'
    print '3) Show graphs'
    print '4) Save & exit'
    print '5) Close without saving'
    choose = int(raw_input())

    if(choose == 1):
        print '\n\nAdd operation:'
        print 'Step 1. Write sum:'
        value = float(raw_input())
        print 'Step 3. Shoose direction (0 - input, 1 - output):'
        direction = int(raw_input())
        print '(Advanced)'
        print 'Step 2. Write name:'
        name = raw_input()
        print 'Step 4. Write tags (splitted by \';\'):'
        tags_line = raw_input()
        tags = tags_line.split(';')
        dt = datetime.today()
        op = Operation(name, tags, value, direction, dt)
        f.addOperation(op)

        print 'Complete!\n\n'
    
    if(choose == 2):
        print '\n\nYour operations:'
        print f.getOperationsInfo()
        print '\n'

    if(choose == 20):
        print '\n\nYour operations:'
        print f.getOperationsInfo_short()
        print '\n'
    
    if(choose == 3):
        f.drawPlots(datetime.today())
    
    if(choose == 4):
        print 'Saving file...'
        f.save(filename)
        print 'File save in \'' + filename + '\'.'
        break
    
    if(choose == 5):
        break

print 'Closing...'

