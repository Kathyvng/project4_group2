function fillzipcode(){
    const city = document.getElementById('city').value;
    let options=[];
    if(city ==="Auburn"){ 
        options =['98001','98092','98002']
    } else if (city === "Bellevue"){
        options =['98006','98004','98008','98005','98007']
    } else if (city === "Federal Way"){
        options =['98023','98003']
    } else if (city === "Kent"){
        options =['98042','98031','98030','98032']
    } else if (city === "Kirkland"){
        options =['98034','98033']
    } else if (city === "Redmond"){
        options =['98052','98053']
    } else if (city === "Renton"){
        options =['98059','98058','98056','98055']
    } else if (city === "Sammamish"){
        options =['98074','98075','98103']
    } else if (city === "Seattle"){
        options =['98103','98115','98117','98118','98133','98135','98125','98126','98144','98106','98116','98199','98122','98146','98198','98112','98168','98107','98136','98178','98177','98166','98105','98108','98119','98119','98188','98109','98102','98148'] 
    }

    const zipcode = document.getElementById('zipcode');
   
options.forEach((optioninput) => {
    const option = document.createElement('option');
    option.value = optioninput;
    option.textContent = optioninput;
    zipcode.appendChild(option);
}
)};

document.getElementById('city').addEventListener('change',fillzipcode);