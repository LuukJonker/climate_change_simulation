from math import pi, log

earth_radius = 6_371_000
height_atmosphere = 6000

circle = earth_radius**2 * pi
globe = 4 * earth_radius**2 * pi
atmosphere_globe = 4 * (earth_radius + height_atmosphere)**2 * pi

solar_constant = 1360

albedo = .33
absorption = .78
cloud_albedo = .26

ppm = 270

options = [0.73 + 3.9*10 ** -7 * ppm**2, 0.69 + 2.5 * 10 ** -4 * ppm, 0.31 + 8.0 * 10 ** -2 * log(ppm),
           -0.14 + ppm/(ppm + 31)]

print(options)

power_sun = circle * solar_constant
power_returned = 0

temperature = None
temperature_atmosphere = None
last_temp = ""
steps = 0

for index, absorption in enumerate(options):
    for i in range(100):
        steps += 1
        power_incoming = power_sun + power_returned
        power_absorbed = power_incoming * (1 - albedo)
        last_temp = temperature
        temperature = (power_absorbed / (5.670373 * 10 ** -8 * globe)) ** 0.25 - 273.15
        power_radiated = power_absorbed
        power_returned = power_radiated * cloud_albedo
        power_atmosphere = absorption * power_radiated * (1 - cloud_albedo)
        temperature_atmosphere = (power_atmosphere/(5.670373 * 10 ** -8 * atmosphere_globe * absorption)) ** 0.25-273.15
        power_returned += power_atmosphere / 2

    print(f"Option { index }, with a absorption of { absorption }, gave a land temperature of { temperature } "
          f"and a atmospheric temperature of { temperature_atmosphere}")
