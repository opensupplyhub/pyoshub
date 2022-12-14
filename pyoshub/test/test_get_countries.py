import pytest
import pyoshub.pyoshub as pyoshub
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [
            ('authorization', 'HIDDEN')],
        "record_mode": 'new',
        "ignore_localhost": True
    }


@pytest.mark.vcr()
class Test_get_countries:
    def test_get_countries(self):
        osh_api = pyoshub.OSH_API(
            url=os.environ["TEST_OSH_URL"],
            token=os.environ["TEST_OSH_TOKEN"],
            check_token=True)
        result = osh_api.get_countries()
        assert (len(result) == 250)
        assert ('iso_3166_2' in result[0].keys())
        assert ('country' in result[0].keys())
        assert (result == [
            {'iso_3166_2': 'AF', 'country': 'Afghanistan'},
            {'iso_3166_2': 'AX', 'country': 'Åland Islands'},
            {'iso_3166_2': 'AL', 'country': 'Albania'},
            {'iso_3166_2': 'DZ', 'country': 'Algeria'},
            {'iso_3166_2': 'AS', 'country': 'American Samoa'},
            {'iso_3166_2': 'AD', 'country': 'Andorra'},
            {'iso_3166_2': 'AO', 'country': 'Angola'},
            {'iso_3166_2': 'AI', 'country': 'Anguilla'},
            {'iso_3166_2': 'AQ', 'country': 'Antarctica'},
            {'iso_3166_2': 'AG', 'country': 'Antigua and Barbuda'},
            {'iso_3166_2': 'AR', 'country': 'Argentina'},
            {'iso_3166_2': 'AM', 'country': 'Armenia'},
            {'iso_3166_2': 'AW', 'country': 'Aruba'},
            {'iso_3166_2': 'AU', 'country': 'Australia'},
            {'iso_3166_2': 'AT', 'country': 'Austria'},
            {'iso_3166_2': 'AZ', 'country': 'Azerbaijan'},
            {'iso_3166_2': 'BS', 'country': 'Bahamas'},
            {'iso_3166_2': 'BH', 'country': 'Bahrain'},
            {'iso_3166_2': 'BD', 'country': 'Bangladesh'},
            {'iso_3166_2': 'BB', 'country': 'Barbados'},
            {'iso_3166_2': 'BY', 'country': 'Belarus'},
            {'iso_3166_2': 'BE', 'country': 'Belgium'},
            {'iso_3166_2': 'BZ', 'country': 'Belize'},
            {'iso_3166_2': 'BJ', 'country': 'Benin'},
            {'iso_3166_2': 'BM', 'country': 'Bermuda'},
            {'iso_3166_2': 'BT', 'country': 'Bhutan'},
            {'iso_3166_2': 'BO', 'country': 'Bolivia, Plurinational State of'},
            {'iso_3166_2': 'BQ', 'country': 'Bonaire, Sint Eustatius and Saba'},
            {'iso_3166_2': 'BA', 'country': 'Bosnia and Herzegovina'},
            {'iso_3166_2': 'BW', 'country': 'Botswana'},
            {'iso_3166_2': 'BV', 'country': 'Bouvet Island'},
            {'iso_3166_2': 'BR', 'country': 'Brazil'},
            {'iso_3166_2': 'IO', 'country': 'British Indian Ocean Territory'},
            {'iso_3166_2': 'BN', 'country': 'Brunei Darussalam'},
            {'iso_3166_2': 'BG', 'country': 'Bulgaria'},
            {'iso_3166_2': 'BF', 'country': 'Burkina Faso'},
            {'iso_3166_2': 'BI', 'country': 'Burundi'},
            {'iso_3166_2': 'KH', 'country': 'Cambodia'},
            {'iso_3166_2': 'CM', 'country': 'Cameroon'},
            {'iso_3166_2': 'CA', 'country': 'Canada'},
            {'iso_3166_2': 'CV', 'country': 'Cape Verde'},
            {'iso_3166_2': 'KY', 'country': 'Cayman Islands'},
            {'iso_3166_2': 'CF', 'country': 'Central African Republic'},
            {'iso_3166_2': 'TD', 'country': 'Chad'},
            {'iso_3166_2': 'CL', 'country': 'Chile'},
            {'iso_3166_2': 'CN', 'country': 'China'},
            {'iso_3166_2': 'CX', 'country': 'Christmas Island'},
            {'iso_3166_2': 'CC', 'country': 'Cocos (Keeling) Islands'},
            {'iso_3166_2': 'CO', 'country': 'Colombia'},
            {'iso_3166_2': 'KM', 'country': 'Comoros'},
            {'iso_3166_2': 'CG', 'country': 'Congo'},
            {'iso_3166_2': 'CD', 'country': 'Congo, the Democratic Republic of the'},
            {'iso_3166_2': 'CK', 'country': 'Cook Islands'},
            {'iso_3166_2': 'CR', 'country': 'Costa Rica'},
            {'iso_3166_2': 'CI', 'country': "Côte d'Ivoire"},
            {'iso_3166_2': 'HR', 'country': 'Croatia'},
            {'iso_3166_2': 'CU', 'country': 'Cuba'},
            {'iso_3166_2': 'CW', 'country': 'Curacao'},
            {'iso_3166_2': 'CY', 'country': 'Cyprus'},
            {'iso_3166_2': 'CZ', 'country': 'Czech Republic'},
            {'iso_3166_2': 'DK', 'country': 'Denmark'},
            {'iso_3166_2': 'DJ', 'country': 'Djibouti'},
            {'iso_3166_2': 'DM', 'country': 'Dominica'},
            {'iso_3166_2': 'DO', 'country': 'Dominican Republic'},
            {'iso_3166_2': 'EC', 'country': 'Ecuador'},
            {'iso_3166_2': 'EG', 'country': 'Egypt'},
            {'iso_3166_2': 'SV', 'country': 'El Salvador'},
            {'iso_3166_2': 'GQ', 'country': 'Equatorial Guinea'},
            {'iso_3166_2': 'ER', 'country': 'Eritrea'},
            {'iso_3166_2': 'EE', 'country': 'Estonia'},
            {'iso_3166_2': 'ET', 'country': 'Ethiopia'},
            {'iso_3166_2': 'FK', 'country': 'Falkland Islands (Malvinas)'},
            {'iso_3166_2': 'FO', 'country': 'Faroe Islands'},
            {'iso_3166_2': 'FJ', 'country': 'Fiji'},
            {'iso_3166_2': 'FI', 'country': 'Finland'},
            {'iso_3166_2': 'FR', 'country': 'France'},
            {'iso_3166_2': 'GF', 'country': 'French Guiana'},
            {'iso_3166_2': 'PF', 'country': 'French Polynesia'},
            {'iso_3166_2': 'TF', 'country': 'French Southern Territories'},
            {'iso_3166_2': 'GA', 'country': 'Gabon'},
            {'iso_3166_2': 'GM', 'country': 'Gambia'},
            {'iso_3166_2': 'GE', 'country': 'Georgia'},
            {'iso_3166_2': 'DE', 'country': 'Germany'},
            {'iso_3166_2': 'GH', 'country': 'Ghana'},
            {'iso_3166_2': 'GI', 'country': 'Gibraltar'},
            {'iso_3166_2': 'GR', 'country': 'Greece'},
            {'iso_3166_2': 'GL', 'country': 'Greenland'},
            {'iso_3166_2': 'GD', 'country': 'Grenada'},
            {'iso_3166_2': 'GP', 'country': 'Guadeloupe'},
            {'iso_3166_2': 'GU', 'country': 'Guam'},
            {'iso_3166_2': 'GT', 'country': 'Guatemala'},
            {'iso_3166_2': 'GG', 'country': 'Guernsey'},
            {'iso_3166_2': 'GN', 'country': 'Guinea'},
            {'iso_3166_2': 'GW', 'country': 'Guinea-Bissau'},
            {'iso_3166_2': 'GY', 'country': 'Guyana'},
            {'iso_3166_2': 'HT', 'country': 'Haiti'},
            {'iso_3166_2': 'HM', 'country': 'Heard Island and McDonald Islands'},
            {'iso_3166_2': 'VA', 'country': 'Holy See (Vatican City State)'},
            {'iso_3166_2': 'HN', 'country': 'Honduras'},
            {'iso_3166_2': 'HK', 'country': 'Hong Kong'},
            {'iso_3166_2': 'HU', 'country': 'Hungary'},
            {'iso_3166_2': 'IS', 'country': 'Iceland'},
            {'iso_3166_2': 'IN', 'country': 'India'},
            {'iso_3166_2': 'ID', 'country': 'Indonesia'},
            {'iso_3166_2': 'IR', 'country': 'Iran, Islamic Republic of'},
            {'iso_3166_2': 'IQ', 'country': 'Iraq'},
            {'iso_3166_2': 'IE', 'country': 'Ireland'},
            {'iso_3166_2': 'IM', 'country': 'Isle of Man'},
            {'iso_3166_2': 'IL', 'country': 'Israel'},
            {'iso_3166_2': 'IT', 'country': 'Italy'},
            {'iso_3166_2': 'JM', 'country': 'Jamaica'},
            {'iso_3166_2': 'JP', 'country': 'Japan'},
            {'iso_3166_2': 'JE', 'country': 'Jersey'},
            {'iso_3166_2': 'JO', 'country': 'Jordan'},
            {'iso_3166_2': 'KZ', 'country': 'Kazakhstan'},
            {'iso_3166_2': 'KE', 'country': 'Kenya'},
            {'iso_3166_2': 'KI', 'country': 'Kiribati'},
            {'iso_3166_2': 'KP', 'country': "Korea, Democratic People's Republic of"},
            {'iso_3166_2': 'KR', 'country': 'Korea, Republic of'},
            {'iso_3166_2': 'XK', 'country': 'Kosovo'},
            {'iso_3166_2': 'KW', 'country': 'Kuwait'},
            {'iso_3166_2': 'KG', 'country': 'Kyrgyzstan'},
            {'iso_3166_2': 'LA', 'country': "Lao People's Democratic Republic"},
            {'iso_3166_2': 'LV', 'country': 'Latvia'},
            {'iso_3166_2': 'LB', 'country': 'Lebanon'},
            {'iso_3166_2': 'LS', 'country': 'Lesotho'},
            {'iso_3166_2': 'LR', 'country': 'Liberia'},
            {'iso_3166_2': 'LY', 'country': 'Libya'},
            {'iso_3166_2': 'LI', 'country': 'Liechtenstein'},
            {'iso_3166_2': 'LT', 'country': 'Lithuania'},
            {'iso_3166_2': 'LU', 'country': 'Luxembourg'},
            {'iso_3166_2': 'MO', 'country': 'Macao'},
            {'iso_3166_2': 'MG', 'country': 'Madagascar'},
            {'iso_3166_2': 'MW', 'country': 'Malawi'},
            {'iso_3166_2': 'MY', 'country': 'Malaysia'},
            {'iso_3166_2': 'MV', 'country': 'Maldives'},
            {'iso_3166_2': 'ML', 'country': 'Mali'},
            {'iso_3166_2': 'MT', 'country': 'Malta'},
            {'iso_3166_2': 'MH', 'country': 'Marshall Islands'},
            {'iso_3166_2': 'MQ', 'country': 'Martinique'},
            {'iso_3166_2': 'MR', 'country': 'Mauritania'},
            {'iso_3166_2': 'MU', 'country': 'Mauritius'},
            {'iso_3166_2': 'YT', 'country': 'Mayotte'},
            {'iso_3166_2': 'MX', 'country': 'Mexico'},
            {'iso_3166_2': 'FM', 'country': 'Micronesia, Federated States of'},
            {'iso_3166_2': 'MD', 'country': 'Moldova, Republic of'},
            {'iso_3166_2': 'MC', 'country': 'Monaco'},
            {'iso_3166_2': 'MN', 'country': 'Mongolia'},
            {'iso_3166_2': 'ME', 'country': 'Montenegro'},
            {'iso_3166_2': 'MS', 'country': 'Montserrat'},
            {'iso_3166_2': 'MA', 'country': 'Morocco'},
            {'iso_3166_2': 'MZ', 'country': 'Mozambique'},
            {'iso_3166_2': 'MM', 'country': 'Myanmar'},
            {'iso_3166_2': 'NA', 'country': 'Namibia'},
            {'iso_3166_2': 'NR', 'country': 'Nauru'},
            {'iso_3166_2': 'NP', 'country': 'Nepal'},
            {'iso_3166_2': 'NL', 'country': 'Netherlands'},
            {'iso_3166_2': 'NC', 'country': 'New Caledonia'},
            {'iso_3166_2': 'NZ', 'country': 'New Zealand'},
            {'iso_3166_2': 'NI', 'country': 'Nicaragua'},
            {'iso_3166_2': 'NE', 'country': 'Niger'},
            {'iso_3166_2': 'NG', 'country': 'Nigeria'},
            {'iso_3166_2': 'NU', 'country': 'Niue'},
            {'iso_3166_2': 'NF', 'country': 'Norfolk Island'},
            {'iso_3166_2': 'MK', 'country': 'North Macedonia'},
            {'iso_3166_2': 'MP', 'country': 'Northern Mariana Islands'},
            {'iso_3166_2': 'NO', 'country': 'Norway'},
            {'iso_3166_2': 'OM', 'country': 'Oman'},
            {'iso_3166_2': 'PK', 'country': 'Pakistan'},
            {'iso_3166_2': 'PW', 'country': 'Palau'},
            {'iso_3166_2': 'PS', 'country': 'Palestine, State of'},
            {'iso_3166_2': 'PA', 'country': 'Panama'},
            {'iso_3166_2': 'PG', 'country': 'Papua New Guinea'},
            {'iso_3166_2': 'PY', 'country': 'Paraguay'},
            {'iso_3166_2': 'PE', 'country': 'Peru'},
            {'iso_3166_2': 'PH', 'country': 'Philippines'},
            {'iso_3166_2': 'PN', 'country': 'Pitcairn'},
            {'iso_3166_2': 'PL', 'country': 'Poland'},
            {'iso_3166_2': 'PT', 'country': 'Portugal'},
            {'iso_3166_2': 'PR', 'country': 'Puerto Rico'},
            {'iso_3166_2': 'QA', 'country': 'Qatar'},
            {'iso_3166_2': 'RE', 'country': 'Reunion'},
            {'iso_3166_2': 'RO', 'country': 'Romania'},
            {'iso_3166_2': 'RU', 'country': 'Russian Federation'},
            {'iso_3166_2': 'RW', 'country': 'Rwanda'},
            {'iso_3166_2': 'BL', 'country': 'Saint Barthelemy'},
            {'iso_3166_2': 'SH', 'country': 'Saint Helena, Ascension and Tristan da Cunha'},
            {'iso_3166_2': 'KN', 'country': 'Saint Kitts and Nevis'},
            {'iso_3166_2': 'LC', 'country': 'Saint Lucia'},
            {'iso_3166_2': 'MF', 'country': 'Saint Martin (French part)'},
            {'iso_3166_2': 'PM', 'country': 'Saint Pierre and Miquelon'},
            {'iso_3166_2': 'VC', 'country': 'Saint Vincent and the Grenadines'},
            {'iso_3166_2': 'WS', 'country': 'Samoa'},
            {'iso_3166_2': 'SM', 'country': 'San Marino'},
            {'iso_3166_2': 'ST', 'country': 'Sao Tome and Principe,Sao Tome And Principe'},
            {'iso_3166_2': 'SA', 'country': 'Saudi Arabia'},
            {'iso_3166_2': 'SN', 'country': 'Senegal'},
            {'iso_3166_2': 'RS', 'country': 'Serbia'},
            {'iso_3166_2': 'SC', 'country': 'Seychelles'},
            {'iso_3166_2': 'SL', 'country': 'Sierra Leone'},
            {'iso_3166_2': 'SG', 'country': 'Singapore'},
            {'iso_3166_2': 'SX', 'country': 'Sint Maarten (Dutch part)'},
            {'iso_3166_2': 'SK', 'country': 'Slovakia'},
            {'iso_3166_2': 'SI', 'country': 'Slovenia'},
            {'iso_3166_2': 'SB', 'country': 'Solomon Islands'},
            {'iso_3166_2': 'SO', 'country': 'Somalia'},
            {'iso_3166_2': 'ZA', 'country': 'South Africa'},
            {'iso_3166_2': 'GS', 'country': 'South Georgia and the South Sandwich Islands'},
            {'iso_3166_2': 'SS', 'country': 'South Sudan'},
            {'iso_3166_2': 'ES', 'country': 'Spain'},
            {'iso_3166_2': 'LK', 'country': 'Sri Lanka'},
            {'iso_3166_2': 'SD', 'country': 'Sudan'},
            {'iso_3166_2': 'SR', 'country': 'Suriname'},
            {'iso_3166_2': 'SJ', 'country': 'Svalbard and Jan Mayen'},
            {'iso_3166_2': 'SZ', 'country': 'Swaziland'},
            {'iso_3166_2': 'SE', 'country': 'Sweden'},
            {'iso_3166_2': 'CH', 'country': 'Switzerland'},
            {'iso_3166_2': 'SY', 'country': 'Syrian Arab Republic'},
            {'iso_3166_2': 'TW', 'country': 'Taiwan'},
            {'iso_3166_2': 'TJ', 'country': 'Tajikistan'},
            {'iso_3166_2': 'TZ', 'country': 'Tanzania, United Republic of'},
            {'iso_3166_2': 'TH', 'country': 'Thailand'},
            {'iso_3166_2': 'TL', 'country': 'Timor-Leste'},
            {'iso_3166_2': 'TG', 'country': 'Togo'},
            {'iso_3166_2': 'TK', 'country': 'Tokelau'},
            {'iso_3166_2': 'TO', 'country': 'Tonga'},
            {'iso_3166_2': 'TT', 'country': 'Trinidad and Tobago'},
            {'iso_3166_2': 'TN', 'country': 'Tunisia'},
            {'iso_3166_2': 'TR', 'country': 'Turkey'},
            {'iso_3166_2': 'TM', 'country': 'Turkmenistan'},
            {'iso_3166_2': 'TC', 'country': 'Turks and Caicos Islands'},
            {'iso_3166_2': 'TV', 'country': 'Tuvalu'},
            {'iso_3166_2': 'UG', 'country': 'Uganda'},
            {'iso_3166_2': 'UA', 'country': 'Ukraine'},
            {'iso_3166_2': 'AE', 'country': 'United Arab Emirates'},
            {'iso_3166_2': 'GB', 'country': 'United Kingdom'},
            {'iso_3166_2': 'US', 'country': 'United States'},
            {'iso_3166_2': 'UM', 'country': 'United States Minor Outlying Islands'},
            {'iso_3166_2': 'UY', 'country': 'Uruguay'},
            {'iso_3166_2': 'UZ', 'country': 'Uzbekistan'},
            {'iso_3166_2': 'VU', 'country': 'Vanuatu'},
            {'iso_3166_2': 'VE', 'country': 'Venezuela, Bolivarian Republic of'},
            {'iso_3166_2': 'VN', 'country': 'Vietnam'},
            {'iso_3166_2': 'VG', 'country': 'Virgin Islands, British'},
            {'iso_3166_2': 'VI', 'country': 'Virgin Islands, U.S.'},
            {'iso_3166_2': 'WF', 'country': 'Wallis and Futuna'},
            {'iso_3166_2': 'EH', 'country': 'Western Sahara'},
            {'iso_3166_2': 'YE', 'country': 'Yemen'},
            {'iso_3166_2': 'ZM', 'country': 'Zambia'},
            {'iso_3166_2': 'ZW', 'country': 'Zimbabwe'}
        ])
