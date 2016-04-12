#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re


class entry:

    def is_spam(self):
        if self.data['Job Title'] == 'Fucknugget':
            print 'spam spam'
            return True

        return False

    def __init__(self, data):
        self.data = data
        if self.is_spam():
            pass

        extra = []
        print self.data
        print '========'

        print self.data['Annual Bonus']
        self.data['Annual Bonus'] = self.parse_money(
            self.data['Annual Bonus'], comment=extra)
        print self.data['Annual Bonus'], extra

    def parse_money(self, string, default_currency='', comment=[]):
        string = string.strip()

        if string == 'pepe stock':
            comment.append('pepe stock')
            return (0.0, 0.0, default_currency)

        if string == '':
            return (0.0, 0.0, default_currency)
        if string == 'NA':
            return (0.0, 0.0, default_currency)

        if string.find('-') > -1:
            split = string.find('-')
            left = string[:split]
            left = self.parse_money(left, default_currency, comment)

            right = string[split + 1:]
            right = self.parse_money(right, default_currency, comment)

            return (left[0], right[1], max(left[2], right[2]))

        if re.search('\([0-9]*\$\)', string) is not None:
            match = re.search('\([0-9]*\$\)', string).group(0)
            rest = string.replace(match, '')
            comment.append(rest)
            return self.parse_money(match[1:-1], default_currency, comment)

        if re.search('\(.*\)', string) is not None:
            m = re.search('\(.*\)', string)
            comment.append(m.group(0))
            return self.parse_money(string.replace(m.group(0), ''),
                                    default_currency, comment)

        prior = string
        string = string.replace(',', '')
        string = string.replace('~', '')
        string = string.replace('€', '')  # note, this is not ascii ?
        string = string.replace('£', '')  # nor this?
        if string != prior:
            return self.parse_money(string, comment=comment)

        if string[0] == '$':
            return self.parse_money(string[1:], 'USD', comment)

        if string[-3:] == 'USD':
            return self.parse_money(string[: -3], 'USD', comment)

        if string[-1] == '$':
            return self.parse_money(string[:-1], 'USD', comment)

        if string[-1] == '%':
            return self.parse_money(string[:-1], 'PCT', comment)

        if string[-1] == 'k' or string[-1] == 'K':
            answer = self.parse_money(string[:-1], comment=comment)
            return (answer[0] * 1000, 1000 * answer[1], answer[2])

        return (float(string), float(string), default_currency)

    def __str__(self):
        return str(self.data)

    def is_spam(self):
        return True

data = []

with open('Salaries - Salaries.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for i, row in enumerate(spamreader):
        print 'line', i
        data.append(entry(row))


print data[10]
