require 'rubygems'  
require 'jazz_money'  
  
javascript_files = [  
  '#*class_dojotools*#Spec.js'  
]  
  
jasmine_spec_files = [  
  '#*class_dojotools*#.js'
]  
  
jazz_money = JazzMoney::Runner.new(javascript_files, jasmine_spec_files)
jazz_money.call 
jazz_money.results.each do |message|
  exit 1 unless message[1].to_s.include? "resultpassedmessagesmessagePassed."
end
