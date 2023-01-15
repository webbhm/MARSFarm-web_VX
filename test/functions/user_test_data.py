user = {'email': 'Webb.Howard@gmail.com',
        'domain': 'OpenAgBloom'
        }
access={'farms': [{'name':'OpenAgBloom',
                 'id': 34,
                 'type': 'admin',
                 'experiments': [{'name': 'Exp1',
                          'trials':[{'name': 'Trial1',
                                   'id':123,
                                   'status': 'Complete'},
                                  {'name': 'Trail2',
                                   'id':567,
                                   'status': 'In_Process'}
                                  ]  # end trials
                                }, # end experiment
                            {'name': 'Exp2',
                            'trials':[{'name': 'Trial3',
                                     'id':'abc',
                                     'status': 'Complete'},
                                  {'name': 'Trail4',
                                   'id':789,
                                   'status': 'Complete'}
                                    ] # end trials
                             } # end experiment
                            ] # end eperiments
                         } # end school
                ], # end schools
		'defaults':{'farm':'OpenAgBloom', 'experiment':'Exp2' , 'trial':'Trail4'}
                 } # end access

defaults={'farm':'OpenAgBloom', 'experiment':'Exp2' , 'trial':'Trail4'}