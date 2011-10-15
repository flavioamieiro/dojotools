from datetime import datetime
import os
import sys
import re

GENERATOR_MESSAGES = {
    'error': 'Generator failed to generate files',
    'message': "Generating Folder...",
    'lang': "Language found: %s",
    'lang_error': "%s generator wasn't found",
    'exists': "Dojo path already exists!",
}

join = lambda a, b: os.path.join(os.path.abspath(a), b)

def sprint(text, show):
    if show:
        print text

class Generator(object):
    
    def __init__(self, args, messages = GENERATOR_MESSAGES):
        self.opts = args.split(" ")
        self.errors = []

        self.language = ""
        self.problem_name = ""
        self.extra_name = ""
        
        self.today = datetime.today().strftime("%Y%m%d")
        
        self.folder_name = ""
        self.folder_path = ""
        self.generator_path = ""
        self.capitalized_name = ""
        
        self.messages = messages

        
    def show_errors(self, show):
        for error in self.errors:
            sprint(error, show)    
        return False
        
    def parse_opts(self, show=True):
        if len(self.opts) < 2:
            self.errors.append(self.messages['error'])
        self.show_errors(show)
        return not bool(self.errors) 
    
    def read_opts(self, show=True):
        if self.errors:
            return self.show_errors(show)
        self.language = self.opts.pop(0)
        self.problem_name = self.opts.pop(0)
        self.extra_name = "_".join(self.opts)
        if self.extra_name:
            self.extra_name = "_" + self.extra_name

        self.folder_name = "%s%s_%s_%s" %(
            self.today, 
            self.extra_name, 
            self.language, 
            self.problem_name
        )
        
        self.folder_path = join(os.path.curdir, self.folder_name)
        self.generator_path = join(os.path.dirname(__file__), "generators/%s/" %(self.language))
        
        splitted_name =  self.problem_name.split('_')
        
        snake_case = self.problem_name
        pascal_case = ''.join(part.capitalize() for part in splitted_name)
        down_case = ''.join(splitted_name)
        camel_case = splitted_name.pop(0) + ''.join([part.capitalize() for part in splitted_name])
        
        self.cases = {
        
            '#_#dojotools#_#' : snake_case,
            '#_#class_dojotools#_#' : pascal_case,
            '#_#down_dojotools#_#' : down_case,
            '#_#camel_dojotools#_#' : camel_case,
            
        
        }

        
        return True

    def replace(self, text):
        for sub, replace in self.cases.iteritems():
            text = re.sub(sub, replace, text) 
        return text

    def copy_and_rename(self, current, folder_name, original):
        isdir = lambda x: os.path.isdir(x) and not os.path.islink(x)        

        folder_path = join(current, folder_name)
        os.mkdir(folder_path)
        file_list = os.listdir(original)
        for infile in file_list:
            gen_path = join(original, infile) 
            if isdir(gen_path):
                self.copy_and_rename(folder_path, infile, gen_path)
            else:
                new_path = join(folder_path,self.replace(infile))
                #with open(new_path, 'w') as w, open(gen_path, 'r') as r: #python 2.7
                with open(new_path, 'w') as w:
                    with open(gen_path, 'r') as r:
                        for line in r:
                            w.write(self.replace(line))
        
    def generate(self, show=True):
        if self.errors:
            return self.show_errors(show)
        if not os.path.exists(self.folder_path):
            sprint(self.messages['message'], show)

            if os.path.exists(self.generator_path):
                sprint(self.messages['lang'] %(self.language), show)
                self.copy_and_rename(os.path.curdir, self.folder_name, self.generator_path)
            else:
                self.errors.append(self.messages['lang_error'] %(self.language))
                self.show_errors(show)
        else:
            self.errors.append(self.messages['exists'])
            self.show_errors(show)
            
        return not bool(self.errors)           

    def generated(self):
        return ((not self.errors) or self.messages['exists'] in self.errors)     


def generate(generate, directory, messages):
    generator = Generator(generate, messages=messages)
    if generate and generator.parse_opts():
        generator.read_opts()
        generator.generate() 
        if generator.generated() and directory == os.path.abspath(os.path.curdir):  
            return generator.folder_path
    return directory

if __name__ == '__main__':
    args = sys.argv
    args.pop(0)
    generator = Generator(' '.join(args), messages=GENERATOR_MESSAGES)
    if generator.parse_opts():
        generator.read_opts()
        generator.generate() 
        
             

