# scrapy
Паук для datacvr.virk.dk
Информация о выполеннии.    
Изначальная страница:   
"https://datacvr.virk.dk/data/index.php?antal_ansatte=null&region=hovedstaden%2Csjaelland%2Csyddanmark%2Cmidtjylland%2Cnordjylland%2Cgroenland&soeg=&q=visninger&language=en-gb"    
С данной страницы извлекается cvr код, с помощью которого мы переходим на страницу компании по следующему шаблону:  
"https://datacvr.virk.dk/data/index.php?antal_ansatte=null&enhedstype=virksomhed&id={cvr}&region=hov&q=visenhed&language=en-gb?", где cvr который мы извлекли.  

table_1 - заголовки/ключи с основной страницы   
table_2 - информация с основной странице в виде html кода. Который потом конвертировался в инфорамациию функции convert 
table_3 - заголовки/ключи для expanded_business_information 
table_4 - информация для expanded_business_informationв виде html кода. Который потом конвертировался в инфорамациию функции convert     
table_5 - заголовки/ключи для power_to_bind_and_key_individuals_and_auditor 
table_6 - информация для power_to_bind_and_key_individuals_and_auditor виде html кода. Который потом конвертировался в инфорамациию функции convert_power_to_bind_and_key_individuals_and_auditor   
table_7 -  заголовки/ключи для convert_ownership 
table_8 -  информация для ownership виде html кода. Который потом конвертировался в инфорамациию функции convert_ownership  
table_9 - заголовки/ключи для information_on_main_company   
table_10 - информация для information_on_main_company в виде html кода. Который потом конвертировался в инфорамациию функции convert    
table_11 - заголовки/ключи для production_units     
table_12 - информация для production_units в виде html кода. Который потом конвертировался в инфорамациию функции convert   
table_10 - информация для history в виде html кода. Который потом конвертировался в инфорамациию функции convert_history    

По умолчанию выключены табдицы 5-8, есть возможность включить(откоментировать), но количество обробатаемых комапний сократиться на 30%.

Переключением по стронице осуществляются по следующему шаблону: 
"https://datacvr.virk.dk/data/index.php?page={self.count}antal_ansatte=null&region=hovedstaden%2Csjaelland%2Csyddanmark%2Cmidtjylland%2Cnordjylland%2Cgroenland&soeg=&q=visninger&language=en-gb", где self.count номер страницы, по умаолчанию стоит 150 страниц(page_count = 150)

Все данные сохроняются в mangodb имя коллекции хрониться в pipelines.py, переменная: collection_name = 'information', имя DB в settings.py, переменная: MONGO_DATABASE = 'scrapy'   
Так же рекомендуется переимановать переменную  ITEM_PIPELINES = {'learn.pipelines.MongoPipeline': 300}, где вместо learn будет имя вашего scrapy проекта.

Запуск осуществляется, через команду в термнале: 'scrapy crawl datacvr_virk'
