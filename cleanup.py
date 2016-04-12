#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re


class entry:

    def __init__(self, data):
        self.data = data

        if self.is_spam():
            return

        extra = []
        self.data['Annual Bonus'] = self.parse_money(
            self.data['Annual Bonus'], comment=extra)
        extra = []
        self.data['Annual Base Pay'] = self.parse_money(
            self.data['Annual Base Pay'], comment=extra)

        extra = []
        print self.data
        print '========'

        print self.data['Signing Bonus']
        self.data['Signing Bonus'] = self.parse_money(
            self.data['Signing Bonus'], comment=extra)
        print self.data['Signing Bonus'], extra

    def is_spam(self):
        blacklisted_words = (
            'Fucknugget', 'YerAnus', 'a box of lube', 'SEXUAL',
            '2 rare pepes', 'I don\'t do anal', 'GNU fatshit foundation',
            'ALLAH HU AKBAR', 'FUCKING ', 'Hang yourself ', 'Your mom',
            'What the fuck did you just fucking say about me, you little bitch?',
            '2\xf0\x9f\x8c\x9d,\xf0\x9f\x8c\x9d\xf0\x9f\x8c\x9d\xf0\x9f\x8c\x9d USD',
            'Prince Vegeta', 'poopfeast420', 'the nazi party of america', '\xe3\x85\x81'
        )

        for key in self.data:
            if self.data[key] in blacklisted_words:
                return True

        greylisted_words = ('asdf')
        score = 0

        for key in self.data:
            if self.data[key] in greylisted_words:
                score += 1
        if score > 5:
            return True

        return False

    def parse_money(self, string, default_currency='', comment=[]):
        string = string.strip()

        zero_strings = (
            '', 'NA', 'na', 'O', 'no', 'N/a', 'No', 'None', 'ha', 'n/a', 'N/A',
            'none', 'nothing')
        if string in zero_strings:
            return (0.0, 0.0, default_currency)

        leq_strings = ('<=', 'up to', 'Up to ')
        for match in leq_strings:
            length = len(match)
            if string[:length] == match:
                answer = self.parse_money(
                    string[length:], default_currency, comment)
                return (0, answer[1], answer[2])

        regex = '^([0-9]*.?[0-9]*) vested over 4 years$'
        if re.match(regex, string) is not None:
            number = re.search(regex, string).group(1)
            rest = 'per year vested over 4 years'
            comment.append(rest)
            answer = self.parse_money(number, default_currency, comment)
            return (answer[0] / 4, answer[1] / 4, answer[2])

        if re.match('^([0-9]*)\*([0-9]*)$', string) is not None:
            match = re.match('^([0-9]*)\*([0-9]*)$', string)
            a, b = match.group(1), match.group(2)
            a = self.parse_money(a, default_currency, comment)
            b = self.parse_money(b, default_currency, comment)
            return (a[0] * b[0], a[1] * b[1], max(a[2], b[2]))

        regex = '\([0-9]*\$?\)'
        if re.search(regex, string) is not None:
            match = re.search(regex, string).group(0)
            rest = string.replace(match, '')
            comment.append(rest)
            return self.parse_money(match[1: -1], default_currency, comment)

        if re.search('\(.*\)', string) is not None:
            m = re.search('\(.*\)', string)
            comment.append(m.group(0))
            return self.parse_money(string.replace(m.group(0), ''),
                                    default_currency, comment)

        comment_strings = (
            'Performance pay',
            'of Base Pay', 'of Salary', 'of base', 'monthly salary increment', 'of salary',
            'Profit Share Bonus', 'cash', 'but that NEVER happens', 'Unknown',
            'Yes', 'TBD', 'pay', '¯\__/¯', '2nd year', 'Varies on performance,',
            'of annual for exceeding', 'ca.', 'depending on performance',
            'target', 'Base', 'yearly salary', 'Annual Pay', 'Varies',
            'depends on business /', 'Variable', 'Between', '90000 BRL / ', 'corp2corp no bennies',
            '£42000 / ', 'after TAX', '~27.2KUSD by today\'s rate')
        for match in comment_strings:
            if string.find(match) > -1:
                comment.append(match)
                string = string.replace(match, '')
                return self.parse_money(string, default_currency, comment)

        range_strings = ('-', ' or ', ' and ')
        for match in range_strings:
            length = len(match)

            if string.find(match) > -1:
                split = string.find(match)
                left = string[:split]
                left = self.parse_money(left, default_currency, comment)

                right = string[split + length:]
                right = self.parse_money(right, default_currency, comment)

                return (left[0], right[1], max(left[2], right[2]))

        prior = string
        string = string.replace(',', '')
        string = string.replace('\'', '')
        string = string.replace('~', '')
        string = string.replace('?', '')
        string = string.replace(' ', '')
        string = string.replace('/YEAR', '')
        string = string.replace(':', '')
        string = string.replace('/yr', '')
        if string != prior:
            return self.parse_money(string, default_currency, comment)

        currency_indicators = (
            ('USD', 'USD'), ('GBP', 'GBP'), ('$', 'USD'), ('€', 'EUR'),
            ('pounds', 'GBP'), ('£', 'GBP'), ('₹', 'INR'), ('CNY', 'CNY'),
            ('$', 'USD'), ('NZD', 'NZD'), ('HKD', 'HKD'), ('%', 'PCT'),
            ('HK$', 'HKD'), ('EUR', 'EUR'), ('CHF', 'CHF'), ('JPY', 'JPY'),
            ('INR', 'INR'), ('Eur', 'EUR'), ('¥', 'JPY'), ('yen', 'JPY'),
            ('CAD', 'CAD'), ('SEK', 'SEK'), ('PLN', 'PLN'), ('ZAR', 'ZAR'),
            ('NOK', 'NOK'), ('euros', 'EUR'), ('gbp', 'GBP'), ('DKK', 'DKK'),
            ('PKR', 'PKR'), ('CAN$', 'CAD'), ('euro', 'EUR'), ('AUD', 'AUD'),
            ('nzd', 'NZD'), ('R$', 'BRL'), ('NZ$', 'NZD'), ('Euro', 'EUR'),
            ('CDN', 'CAD'), ('HUF', 'HUF'), ('rubles', 'RUB'), ('SGD', 'SGD'),
            ('Aud', 'AUD'), ('Rs', 'INR'), ('RMB', 'CNY'), ('RUB', 'RUB'),
            ('e', 'EUR'), ('EURO', 'EUR'), ('eur', 'EUR'), ('BRL', 'BRL'))
        for indicator in currency_indicators:
            (special_string, currency) = indicator
            match_length = len(special_string)

            if string[: match_length] == special_string:
                return self.parse_money(string[match_length:], currency, comment)
            if string[-match_length:] == special_string:
                return self.parse_money(string[: -match_length], currency, comment)

        if string[-1] == 'k' or string[-1] == 'K':
            answer = self.parse_money(string[: -1], default_currency, comment)
            return (answer[0] * 1000, 1000 * answer[1], answer[2])

        if string[-3:] == '万':
            answer = self.parse_money(
                string[: -3] + 'JPY', default_currency, comment)
            return (answer[0] * 10 ** 4, 10 ** 4 * answer[1], answer[2])

        if string[-7:] == 'Million':
            answer = self.parse_money(string[: -7], default_currency, comment)
            return (answer[0] * 10 ** 7, 10 ** 7 * answer[1], answer[2])

        if string[-1:] == 'M':
            answer = self.parse_money(string[: -1], default_currency, comment)
            return (answer[0] * 10 ** 7, 10 ** 7 * answer[1], answer[2])

        if string[-3:] == '/hr':
            answer = self.parse_money(string[: -3], default_currency, comment)
            return (answer[0] * 40 * 50, 40 * 50 * answer[1], answer[2])

        if string[-7:] == 'perhour':
            answer = self.parse_money(string[: -7], default_currency, comment)
            return (answer[0] * 40 * 50, 40 * 50 * answer[1], answer[2])

        if string[-5:] == '/hour':
            answer = self.parse_money(string[: -5], default_currency, comment)
            return (answer[0] * 40 * 50, 40 * 50 * answer[1], answer[2])

        if string[-2:] == 'hr':
            answer = self.parse_money(string[: -2], default_currency, comment)
            return (answer[0] * 40 * 50, 40 * 50 * answer[1], answer[2])

        if string[-4:] == 'hour':
            answer = self.parse_money(string[: -4], default_currency, comment)
            return (answer[0] * 40 * 50, 40 * 50 * answer[1], answer[2])

        if string[-4:] == '/day':
            answer = self.parse_money(string[: -4], default_currency, comment)
            return (answer[0] * 5 * 50, 5 * 50 * answer[1], answer[2])

        return (float(string), float(string), default_currency)

    def __str__(self):
        return str(self.data)


data = []

with open('Salaries - Salaries.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for i, row in enumerate(spamreader):
        print 'line', i
        data.append(entry(row))


print data[10]
