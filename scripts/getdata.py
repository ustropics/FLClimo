import mechanize

url = 'https://climatecenter.fsu.edu/climate-data-access-tools/downloadable-data'

br = mechanize.Browser()

# set options to simulate a browser
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

response = br.open(url)

# select the first form on the page
br.select_form(nr=1)

br.form.controls[0].value = ['80228']
br.form.controls[4].value = ['12']
br.form.controls[5].value = ['31']
br.form.controls[6].value = ['2022']
br.form.controls[7].value = ['all']

for control in br.form.controls:
    print(control)

br.submit(name='down_Submit')