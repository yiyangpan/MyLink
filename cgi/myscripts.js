function addNewListItem(){
		var htmlSelect=document.getElementById('selectYear');
		var optionValue=document.getElementById('txtYearValue');

		if(optionValue.value==''){
			alert('please enter option value');
			optionValue.focus();
			return false;
		}
		if(isOptionAlreadyExist(htmlSelect,optionValue.value)){
			alert('Option value already exists');
			optionValue.focus();
			return false;
		}
		if(isOptionAlreadyExist(htmlSelect,optionValue.value)){
			alert('value already exists');
			optionValue.focus();
			return false;
		}
		var selectBoxOption = document.createElement("option");
		selectBoxOption.value = optionValue.value;
		selectBoxOption.text = optionValue.value;
		htmlSelect.add(selectBoxOption, null); 
		alert("Option has been added successfully");
		return true;

	}
	function isOptionAlreadyExist(listBox,value){
		var exists=false;
		for(var x=0;x<listBox.options.length;x++){
			if(listBox.options[x].value==value || listBox.options[x].text==value){ 
			exists=true;
			break;
			}
		}
		return exists;
	}
	function removeListItem(){
		var htmlSelect=document.getElementById('selectYear');

		if(htmlSelect.options.length==0){
			alert('You have removed all options');
			return false;
		}
		var optionToRemove=htmlSelect.options.selectedIndex;
		htmlSelect.remove(optionToRemove);
		alert('The selected option has been removed successfully');
		return true;
	}
