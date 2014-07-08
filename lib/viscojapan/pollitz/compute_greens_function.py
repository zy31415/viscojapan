from os.path import join, basename

from viscojapan.pollitz.pollitz_wrapper import stat2gA, strainA
from dpool import Task, DPool

class ComputeGreensFunction(object):
    def __init__(self,
                 epochs,
                 file_sites,
                 earth_file,
                 earth_file_dir,
                 outputs_dir,
                 subflts_files,
                 controller_file,
                 ):
        self.epochs = epochs
        self.file_sites = file_sites
        self.earth_file = earth_file
        self.earth_file_dir = earth_file_dir
        self.subflts_files = subflts_files
        self.controller_file = controller_file
        self.outputs_dir = outputs_dir

        self.tasks = []

    def _gen_out_file(self, file_flt, epoch):
        outf = join(self.outputs_dir,
                    'day_%04d_'%epoch + basename(file_flt) + '.out')
        return outf

    def _stat2gA(self, file_flt):
        cmd = stat2gA(
            earth_model_stat = self.earth_file,
            stat0_out = join(self.earth_file_dir,'stat0.out'),
            file_flt = file_flt,
            file_sites = self.file_sites,
            file_out = self._gen_out_file(file_flt, 0),
            if_skip_on_existing_output = True,
            stdout = open('/dev/null', 'w')
            )
        cmd()

    def _straina(self, file_flt, epoch):
        cmd = strainA(
            earth_model = self.earth_file,
            
            decay_out = join(self.earth_file_dir,'decay.out'),
            decay4_out = join(self.earth_file_dir,'decay4.out'),
            vsph_out = join(self.earth_file_dir,'vsph.out'),
            vtor_out = join(self.earth_file_dir,'vtor.out'),

            file_out = self._gen_out_file(file_flt, epoch),
            file_flt = file_flt,
            file_sites = self.file_sites,

            days_after = epoch,

            if_skip_on_existing_output = True,
            stdout = open('/dev/null', 'w'),
            stderr = None,
            )
        cmd()
        
    def _load_tasks(self, epoch):
        if epoch == 0:
            for f in self.subflts_files:
                self.tasks.append(
                    Task(target = self._stat2gA, args = (f,)))
        else:
            for f in self.subflts_files:
                self.tasks.append(
                    Task(target = self._straina, args = (f, epoch)))

    def load_tasks(self):
        for epoch in self.epochs:
            self._load_tasks(epoch)

    def run(self):
        self.load_tasks()
        dp = DPool(
            tasks = self.tasks,
            controller_file = self.controller_file)

        dp.run() 

    def gen_epochal_file(self):
        pass
