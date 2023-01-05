"""A free software created for the analysis bulk contraction assay image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-08 for version 1.0b1

Main app

"""

from bulkclot import menu

class BulkClotContraction():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        menu()