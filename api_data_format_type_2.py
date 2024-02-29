data = {
    'urlPlatforma': str,
    'procurementStage': str,
    'startDateContract': str,
    'advantages': str,
    'restrictions': str,

    'type': int,  # обязательно
    'title': str,  # обязательно
    'purchaseNumber': str, # обязательно новое
    'fz': str,  # обязательно
    'purchaseType': str,
    'url': str,  # обязательно

    'obesp_z': str,
    'obesp_i': str,
    'sumInPercents': str,

    'price': str,
    'info_about_banking': str,
    'deliveryTerm': str,
    'terms_of_payment': str,
    'deliveryCondition': str,

    'lots': [
                {
                    'region': str,
                    'deliveryPlace': str,
                    'total_info': str,
                    'additionalInfo': str,
                    # предметы закупки
                    'lotItems': [
                                  {'code': str,
                                  'name': str,
                                  'unit': str,
                                  'count': str,
                                  'unit_price': str,
                                  'cost': str,
                                  }
                                ]
                }
    ],
    'attachments': [{'docDescription': str,
                     'url': str,
                     'docType': str,
                     'editorial': str,
                     'printableNoticeForm': str,
                     'docPublished': str,
                     }],

    'procedureInfo': {
        'endDate': "01:11:00 25.01.2023",
        'scoringDate': "01:11:00 25.01.2023",
        'biddingDate': "01:11:00 25.01.2023",
        'publishedDate': "01:11:00 25.01.2023",
        'updatedDte': "01:11:00 25.01.2023",
        'startDate': "01:11:00 25.01.2023",
        'endDateConsiderationPeriodFirstPart': "01:11:00 25.01.2023",
        'endDateConsiderationPeriodSecondPart': "01:11:00 25.01.2023",
        'debriefingDate': "01:11:00 25.01.2023",
        'Rebidding': str,
    },

    'customer': {
        'fullName': str,
        'factAddress': str,
        'inn': str,
        'kpp': str,
        'ogrn': str,
        'okved': str,
        'dateRegistration': str,
        'organizationType': str,
        'organizationLevel': str,
        'nameBudget': str,
        'customerSite': str,
    },

    'contactPerson': {
        'lastName': str,
        'firstName': str,
        'middleName': str,
        'contactPhone': str,
        'contactEMail': str,
        'mailingAddress': str,
    }
}
