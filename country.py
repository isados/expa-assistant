import pycountry as pc
from phonenumbers.phonenumberutil import country_code_for_region

# Obtained from the sheet's dropdown list
COUNTRY_NAMES_LIST = ('Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas, The', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burma', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cabo Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Democratic Republic of the', 'Congo, Republic of the', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia, The', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea, North', 'Korea, South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territories', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe')

incorrect_country_name_resolution = {
'Congo, Democratic Republic of the':'Congo, The Democratic Republic of the',
'Congo, Republic of the':'Congo',
"Cote d'Ivoire":"Côte d'Ivoire",
"Curacao":"Curaçao",
"Burma":"Myanmar",
"Brunei":"Brunei Darussalam",
"Bahamas, The":"Bahamas" ,
"North Korea":"Korea, Democratic People's Republic of",
"Korea, North":"Korea, Democratic People's Republic of",
"South Korea":"Korea, Republic of",
"Korea, South":"Korea, Republic of",
'Gambia, The':'Gambia',
# Previous ISO country names
'Laos':"Lao People's Democratic Republic",
'Macau':'Macao',
'Palestinian Territories':"Palestine, State of",
'Vietnam':"Viet Nam"
}

new_countries = {
'Kosovo':'XK'
}

# Standard Country List from pycountry lib
iso_country_list = sorted([x.name for x in list(pc.countries)])

def int_calling_code(country_name):
    try:
        alpha2 = pc.countries.get(name=country_name).alpha_2
        country_code = country_code_for_region(alpha2)
    except:
        try:
            alpha2 = pc.countries.get(name = incorrect_country_name_resolution[country_name]).alpha_2
            country_code = country_code_for_region(alpha2)
        except:
            try:
                right_one = [cn for cn in iso_country_list if country_name in cn][0]
                alpha2 = pc.countries.get(name=right_one).alpha_2
                country_code = country_code_for_region(alpha2)
            except:
                country_code = country_code_for_region(new_countries[country_name])
    return str(country_code)
