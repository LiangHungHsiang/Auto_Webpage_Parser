require 'capybara'
require 'capybara/dsl'
require 'csv'
require 'parallel'
include Capybara::DSL

Capybara.javascript_driver = :selenum # Capybara 選用的javascript_driver 是selenum
Capybara.current_driver = :selenium # Capybara 選用的html 是selenum
Capybara.register_driver :selenium do |app|
	Capybara::Selenium::Driver.new(app, :browser => :chrome)
end
directory = "Vela_Pulsar/"
year = []
month = []
day = []
hour = []
elevationAngle = []
theta = []
altitude = []
longitude = []
latitude = []

CSV.foreach(File.path(directory + "year.csv")) do |item|
    year << item
end
CSV.foreach(File.path(directory + "month.csv")) do |item|
    month << item
end
CSV.foreach(File.path(directory + "day.csv")) do |item|
    day << item
end
CSV.foreach(File.path(directory + "hour.csv")) do |item|
    hour << item
end
CSV.foreach(File.path(directory + "elevationAngle.csv")) do |item|
    elevationAngle << item
end
# CSV.foreach(File.path(directory + "theta.csv")) do |item|
#     theta << item
# end
CSV.foreach(File.path(directory + "altitude.csv")) do |item|
    altitude << item
end
CSV.foreach(File.path(directory + "longitude.csv")) do |item|
    longitude << item
end
CSV.foreach(File.path(directory + "latitude.csv")) do |item|
    latitude << item
end

lenOfData = year[0].length
#j = 3063.step(lenOfData, 1).to_a
# for i in 0...(lenOfData)
for i in 35859...43063
#Parallel.map(j, in_threads: 2) do |i|
	url = "https://ccmc.gsfc.nasa.gov/modelweb/models/nrlmsise00.php/"
	visit(url)
	find('div#content form input[name="year"]').set(year[0][i])
	monthBtn = all('select[name="month"] option')
	monthBtn[(month[0][i].to_i-1)].click
	find('input[name="day"]').set(day[0][i])
	find('input[name="hour"]').set(hour[0][i])
	find('input[name="latitude"]').set(latitude[0][i])

	if longitude[0][i].to_f < 0
		longitude[0][i] = (longitude[0][i].to_f + 360).to_s
	end

	find('input[name="longitude"]').set(longitude[0][i])
	find('input[name="height"]').set((altitude[0][i].to_f).to_s)
	find('input[name="stop"]').set('100')
	find('input[name="step"]').set('0.25')
	find('input[type="radio"][value="2"][name="format"]').click
	find('input[type="checkbox"][value="10"][name="vars"]').click
	find('input[type="checkbox"][value="11"][name="vars"]').click
	find('input[type="checkbox"][value="12"][name="vars"]').click
	find('input[type="checkbox"][value="13"][name="vars"]').click
	find('input[type="checkbox"][value="14"][name="vars"]').click
	find('input[type="checkbox"][value="15"][name="vars"]').click
	find('input[type="checkbox"][value="16"][name="vars"]').click
	find('input[type="checkbox"][value="17"][name="vars"]').click
	find('input[type="checkbox"][value="18"][name="vars"]').click
	submitBtn = all('input[type="submit"]')
	submitBtn[1].click
	sleep(2)
	find('div#content a').click
	text = find('pre').native.text
	File.write(directory + 'Data_' + i.to_s + '.txt', text)
end