<?

/* Cuidado! PHP 5.4+ apenas */

if(empty($argv[1])) {
    die("Why do you do this to me?\n");
}


class CSV2JSON {

    const DELIMITER = ',';
    const JSON_OPTIONS = JSON_UNESCAPED_UNICODE;

    private $file;
    private $columns = array();

    public function load($filepath) {
        $this->file = fopen($filepath, 'r');
    }

    public function convert($filepath) {
        $this->load($filepath);
        
        $columns = $this->loadColumns();
        
        $output = array();
        
        while($line = $this->getLine()) {
            $output[] = $this->convertLine($line);
        }
        
        echo json_encode($output, self::JSON_OPTIONS);
    }
    
    private function loadColumns() {
        
        $this->columns = array();
        
        $line = $this->getLine();
        
        foreach($line as $index => $name) {
            if(strlen($name)) {
                $this->columns[$index] = $name;
            }
        }
    }
    
    private function getLine() {
        return fgetcsv($this->file, '', self::DELIMITER);
    }
    
    private function convertLine($line) {
        $object = array();
        
        foreach($this->columns as $index => $name) {
            $object[$name] = $line[$index];
        }
        
        return $object;
    }
    
}

$converter = new CSV2JSON();
echo $converter->convert($argv[1]);



