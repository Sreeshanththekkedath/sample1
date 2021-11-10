function visible(){
    var m = document.getElementById('E1')
    if(m.className === 'form-group row invisible'){
        m.className = 'form-group row'
        document.getElementById('A1').className = 'invisible'
    }
}

function invisible(){
    var m = document.getElementById('E1')
    if(m.className === 'form-group row'){
        m.className = 'form-group row invisible'
        document.getElementById('A1').className = 'visible'
    }
}

function visible_1(){
    var m = document.getElementById('E2')
    if(m.className === 'form-group row invisible'){
        m.className = 'form-group row'
        document.getElementById('A2').className = 'invisible'
    }
}

function invisible_1(){
    var m = document.getElementById('E2')
    if(m.className === 'form-group row'){
        m.className = 'form-group row invisible'
        document.getElementById('A2').className = 'visible'
    }
}