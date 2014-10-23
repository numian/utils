require 'nokogiri'
require 'open-uri'
require 'uri'

if ARGV.length != 1
  puts "Usage: ruby #{__FILE__} URI"
  exit 1
end

begin
  page = Nokogiri::HTML open ARGV[0]
  
  links = []
  
  page.css('a').each do |anchor|
    
    if !anchor['href'].nil? and !anchor['href'].empty?
      
      href = anchor['href'].sub(ARGV[0], '')
      href.slice!(/(.*)(#.*)/, 1)
      
      if !links.include? href and href.match '^/.*$'
        links << href
      end
    end
    
  end
  
  uri = URI.parse ARGV[0]
  
  links.each do |link|
  
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = uri.scheme == 'https'
  
    http.start do |session|
      response = session.head link
      
      puts "#{response.code} #{uri.scheme}://#{uri.host}#{link}" unless ['200', '302'].include? response.code
      
    end
  end
  
rescue SocketError => e
  puts "Could not open #{ARGV[0]} (#{e.message})"
  exit 2
end

exit 0