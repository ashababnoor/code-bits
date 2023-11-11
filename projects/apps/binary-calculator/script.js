let op1 = ""
let op2 = ""
let opr = ''
let trk = 0

let counter = 0

let errorMessages = [
    '<span class="red"> Expression error! </span>',
    '<span class="red"> Too large expression! </span>'
]

let zero = document.getElementById('btn0')
let one = document.getElementById('btn1')
let plus = document.getElementById('btnSum')
let sub = document.getElementById('btnSub')
let mult = document.getElementById('btnMul')
let div = document.getElementById('btnDiv')
let res = document.getElementById('res')
let clr = document.getElementById('btnClr')
let eq = document.getElementById('btnEql')

let addText = event => {
    if (op1 === '' && opr === '') {
        clearEve()
    }

    if (errorMessages.includes(res.innerHTML)) {
        res.innerHTML = ''
        console.log('error was encountered')
    }

    if (counter >= 17) {
        clearEve()
        res.innerHTML = errorMessages[1]
        console.log('max length exceeded')
        return
    }

    let element = event.target
    let btn = document.getElementById(element.id + "")
    let text = (btn.innerHTML).replace(/\s/g, "")

    document.getElementById('res').innerHTML += text

    counter = res.innerHTML.length
    console.log('counter:', counter)

    return text
}

let returnText = event => {
    let element = event.target
    let btn = document.getElementById(element.id + "")
    return Number(btn.innerHTML)
}

let clearEve = () => {
    op1 = ''
    op2 = ''
    opr = ''
    trk = 0
    counter = 0
    res.innerHTML = ''
}

let operatorFunc = event => {
    let text = addText(event)
    if (trk === 0) {
        opr = text
        console.log('Operand:', text)
        trk = 1
    } else {
        clearEve()
        console.log('Multiple operand on same expression not allowed')
        res.innerHTML = errorMessages[0]
    }
}

let operandFunc = event => {
    addText(event)

    if (errorMessages.includes(res.innerHTML)) {
        console.log('error was encountered, skipping this turn')
        return
    }

    let str = returnText(event)
    if (trk === 0) {
        op1 += str
    } else {
        op2 += str
    }
    console.log('clicked on', str)
    console.log('Op1:', op1, op1.length)
    console.log('Op2:', op2, op2.length)
}

zero.addEventListener('click', event => {
    operandFunc(event)
})

one.addEventListener('click', event => {
    operandFunc(event)
})

plus.addEventListener('click', event => {
    operatorFunc(event)
})

sub.addEventListener('click', event => {
    operatorFunc(event)
})

mult.addEventListener('click', event => {
    operatorFunc(event)
})

div.addEventListener('click', event => {
    operatorFunc(event)
})

clr.addEventListener('click', clearEve)

eq.addEventListener('click', event => {
    let num1
    let num2
    let result

    if (op1 === '' && opr !== '') {
        clearEve()
        console.log('Operand 1 can\' be empty')
        res.innerHTML = '<span class="red"> Expression error! </span>'
        return
    } else if (op1 === '' && opr === '') {
        clearEve()
        return
    } else {
        num1 = parseInt(op1, 2)
    }

    if (op2 === '') {
        console.log('Only one number clicked:', op1)
        clearEve()
        res.innerHTML = num1.toString(2)
        op1 = num1.toString(2)
        res.innerHTML = op1
        return
    } else {
        num2 = parseInt(op2, 2)
    }

    console.log('Num1:', num1, "Num2:", num2)

    if (opr == '+') {
        result = num1 + num2
    } else if (opr == '-') {
        result = num1 - num2
    } else if (opr == '*') {
        result = num1 * num2
    } else if (opr == '/') {
        result = num1 / num2
    }

    console.log('result:', result)

    clearEve()
    res.innerHTML = result.toString(2)
    op1 = result.toString(2)
})