<?php
include 'SQLConnect.php';

function refValues($arr){
    if (strnatcmp(phpversion(),'5.3') >= 0){ //Reference is required for PHP 5.3+
        $refs = array();
        foreach($arr as $key => $value)
            $refs[$key] = &$arr[$key];
        return $refs;
    }
    return $arr;
}
/* URL Params */
if(isset($_GET["HITType"]))
  $HITType = $_GET["HITType"];
else 
  exit("Provide 'HITType' URL parameter");

if(isset($_GET["workerId"]))
  $workerId = $_GET["workerId"];
else 
  exit("Provide 'workerId' URL parameter");

if(isset($_GET["HITId"])){
  $HITId = $_GET["HITId"];
} else
  exit("Provide 'HITId' URL parameter");

if(isset($_GET["assignmentId"])){
  $HITId = $_GET["assignmentId"];
} else
  exit("Provide 'assignmentId' URL parameter");


if(isset($_GET["action"]))
  $action = $_GET["action"];
else 
  exit("Provide 'action' URL parameter");

if ($action != "check" && $action != "store")
  exit("Must set action=check or action=store; no other values allowed");

if(isset($_GET["tableName"])) {
  $table = $_GET["tableName"];
} else {
  $table = "workerDemographics";
}


// All params are good 
$possibleColumns = array("age","gender","race","politics","otherMinority");
$columnTypes = array("age"=> "i", "gender" => "s","race" => "s", "politics"=> "s",
  "otherMinority"=>"s","HITId" => "s","HITType" => "s","workerId" => "s","assignmentId" => "s");
  
$insertColumns = array("age","gender","race","politics","otherMinority","HITId","HITType","assignmentId");
$conn = SQLconnect();


if ($action == "check") {
  //echo "checking\n";
  $query = "SELECT * FROM ".$table." where workerId = '".$workerId."' ORDER BY insertTime DESC LIMIT 1;";
  //echo $query;
  $rows = array();
  $leastNumNulls = 0;
  $leastNulls = NULL;
  
  if ($result = $conn->query($query)) {

    while ($row = $result->fetch_assoc()){
      echo json_encode($row)."\n";
      //exit();
      /*array_push($rows,$row);
      
      $numNulls = sizeof($row) - sizeof(array_filter(array_values($row)));
      if ($numNulls <= $leastNumNulls)
        $leastNulls = $row;
      */
    }
    //$result->close();
    //echo json_encode($leastNulls);
  }
} else if ($action == "store"){
  /* Checking for more parameters */
  //echo "storing\n";
  $insertValues = array("insertTime" => date("Y-m-d H:i:s"));
  $insertTypes = "s";
  foreach ($_GET as $col => $value){
    if ($col != "action" && $col != "tableName"){
      $insertValues[$col] = $_GET[$col];
      $insertTypes = $insertTypes . $columnTypes[$col];
    }
  }
  $query = "INSERT INTO ".$table." (". implode(', ',array_keys($insertValues)) .") VALUES (". str_repeat("?, ",sizeof($insertValues)-1)."?)";
  array_unshift($insertValues,$insertTypes);
  //echo $query."\n";
  //var_dump($insertValues);
 
  $insert = $conn->prepare($query);
  //echo $insertTypes."\n";
  //echo implode(", ",array_values($insertValues))."\n";
  call_user_func_array(array($insert, 'bind_param'),refValues(array_values($insertValues)));
  
  if ($insert->execute()===TRUE) {
    echo "Record inserted";// into $table!\n";
  } else {
    var_dump($insert);
    echo "Error:".$conn->error;
  }
  $insert->close();
}
?>