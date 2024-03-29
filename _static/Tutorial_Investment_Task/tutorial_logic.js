// This file contains all the js that makes the tutorial work

// FIXME: There's some math errors in the tutorial table!

// Button logic and order handling happens here
$$ = function(x){return document.getElementById(x)};

//first some layout corrections that oTree wouldn't allow otherwise
$$("id_transaction").placeholder = "Amount";
$$("id_transaction2").placeholder = "Amount";

// Also disable the enter key for this page
window.addEventListener('keydown',function(e){
    if(e.keyIdentifier === 'U+000A' || e.keyIdentifier === 'Enter' || e.keyCode === 13) {
        e.preventDefault();
        return false;
    }
}, true);

// Overwrite what the trading-buttons should do:
let buy_buttons = document.getElementsByClassName('buy_button');
let sell_buttons = document.getElementsByClassName('sell_button');
let asset_cont_btn = document.getElementsByClassName('continue_button');
let i;
for (i = 0; i < buy_buttons.length; i++){
    buy_buttons[i].onclick = function() {check_tutorial_moves('buy')};
    sell_buttons[i].onclick = function() {check_tutorial_moves('sell')};
    asset_cont_btn [i].onclick = function() {check_tutorial_moves('continue')};
}

// Keeping track of the tutorial positions
let tutorial_position = 1;
let tutorial_page = 1;
let quiz_position = 1;

// Tutorial flow happens here (checking whether the right buttons are pushed)
check_tutorial_moves = function(action) {
    switch (tutorial_position) {
        case 1: // Buy the asset on page 1
            if (action === 'buy' && $$('id_transaction').valueAsNumber === 2) {
                reveal_next_tutorial_part();
                update_trade_table();
                $$('timer_warning_field').style.visibility = 'shown';  // The one for demonstration purposes
                $$('id_transaction').value = '';
            } else {
                alert('Please buy two shares of the asset.')
            }
        break;
        case 2: // Sell all assets on page 1 to switch to page 2
            if (action === 'sell' && $$('id_transaction').valueAsNumber === 4) {
                reveal_next_tutorial_part();
                $$('trade_continue_button').style.display = 'inline';
                flip_tut_pages('continue');
            } else {
                alert('Please sell all your shares by entering 4 and clicking the "Sell" button.')
            }
            break;
        case 3: // Short the asset by 2 on page 2
            if(tutorial_page === 3) {
                if (action === 'sell' && $$('id_transaction2').valueAsNumber === 4) {
                    reveal_next_tutorial_part();
                    update_trade_table();
                    $$('id_transaction2').value = '';
                } else {
                    alert('Please short the asset by two shares by selling four shares.')
                }
            }
                break;
        case 4: // Jump to holding five shares on page 2 to reveal page 3
            if (action === 'buy' && $$('id_transaction2').valueAsNumber === max_hold + 2 && tutorial_page === 3) {
                reveal_next_tutorial_part();
                flip_tut_pages('continue');
                $$('shorting_continue_button').style.display = 'inline';
            } else {
                alert('Please buy enough shares such that you are holding ' + max_hold + '.')
            }
        break;
        case 5:
            if (tutorial_page === 4){
                reveal_next_tutorial_part()
            } else {
                flip_tut_pages('continue')
            }
        break;
        case 6:
            if (tutorial_page === 4) { reveal_next_tutorial_part() }
            flip_tut_pages('continue');
        break;
        case 7:
            if (tutorial_page === 5){
                if ($$('belief_slider').value === '60') {
                    reveal_next_tutorial_part()
                } else {
                    alert('Please set the slider to 60%!')
                }
            } else {
                flip_tut_pages('continue')
            }
        break;
        default:
            if (action === 'continue'){ // To make navigation possible after having seen everything
                flip_tut_pages('continue')
            }
    }
};

reveal_next_tutorial_part = function(){
    tutorial_position = tutorial_position + 1;

    let elements = document.getElementsByClassName('tut_part_' + (tutorial_position).toString());
    let i;
    for (i = 0; i < elements.length; i++){
        elements[i].style.display = 'inline'
    }
};

flip_tut_pages = function(move){
    let tutorial_index = tutorial_page - 1;

    let page_seq = [$$('content_welcome_page'),
                    $$('content_trading_tutorial'),
                    $$('content_shorting_tutorial'),
                    $$('content_price_movement_tutorial'),
                    $$('content_belief_tutorial'),
                    $$('content_structure_tutorial')];

    window.scrollTo(0, 0);

    if (move === 'continue'){
        if (tutorial_page === page_seq.length){  // If we reached the last page:
            $$('form').submit();
        } else { // Go forward one page
            page_seq[tutorial_index].style.display = 'none';
            page_seq[tutorial_index + 1].style.display = 'inline';
            tutorial_page += 1;
        }
    } else { // Go back one page
        if (tutorial_page !== 1){
            page_seq[tutorial_index].style.display = 'none';
            page_seq[tutorial_index - 1].style.display = 'inline';
            tutorial_page -= 1;
        }
    }
};

update_trade_table = function(){
    if (tutorial_page === 2) {
        $$('new_value').innerHTML = $$('id_price').innerHTML = (start_price + 5).toString();
        $$('id_cash').innerHTML = (start_cash - start_price * 2).toString();
        $$('id_hold').innerHTML = '+4';
        $$('id_return').innerHTML = '20 (' + Math.round((((start_price + 5) /
            start_price) - 1) * 1000) / 10 + ')';
        $$('id_return').style.color = 'limegreen';
        $$('id_baseprice').innerHTML = start_price.toString();
        $$('id_value').innerHTML = ((start_price + 5) * 4).toString();
        $$('id_value_all').innerHTML = (start_cash + 2 * start_price + 4 * 5).toString();
    } else {  // tutorial_page is 3 and we're on the shorting page
        $$('new_value2').innerHTML = $$('id_price2').innerHTML = (start_price - 5).toString();
        $$('id_cash2').innerHTML = (start_cash + start_price).toString();
        $$('id_hold2').innerHTML = '-2';
        $$('id_return2').innerHTML = '10 (' + Math.round((((start_price + 10) /
            start_price) - 1) *1000) / 10 + ')';
        $$('id_return2').style.color = 'limegreen';
        $$('id_baseprice2').innerHTML = start_price.toString();
        $$('id_value2').innerHTML = (start_price - 5 * -2).toString();
        $$('id_value_all2').innerHTML = (start_cash + 5).toString();
    }
};

check_quiz = function(skip_one=false){
    let ans_key = [2, 0, 1, 0, 2, 2];
    // If the answer was correct:
    if ($$('id_Q' + quiz_position + '_' + ans_key[quiz_position - 1]).checked || skip_one){
        if (quiz_position === ans_key.length){
            $$('form').submit();
        } else {
            $$('Q' + quiz_position + '_div').style.display = 'none';
            $$('Q' + (quiz_position + 1).toString() + '_div').style.display = 'inline';
            if (quiz_position === 5){ // Reveal trading table
                $$('quiz_table').style.display = 'inline-table';
            }
            quiz_position += 1;
        }
    } else {  // We got a wrong answer!
        switch (quiz_position) {
            case 1:
                alert('Diese Antwort ist leider falsch.\n\n' +
                    'Aus dem Instruktionstext:\n' +
                    'Welchen der drei möglichen Schritte der Preis beim nächsten Update macht wird zufällig und ' +
                    'mit gleicher Wahrscheinlichkeit gewählt. Lediglich ob der Preis ansteigt oder sinkt wird ' +
                    'durch den oben beschriebenen Mechanismus beeinflusst.');
            break;
            case 2:
                alert('Diese Antwort ist leider falsch.\n\n' +
                    'Aus dem Instruktionstext:\n' +
                    'Wenn es der Firma gut geht, macht diese mit einer höheren Wahrscheinlichkeit Gewinne, ' +
                    'wesswegen der Aktienpreis eher steigen wird. Wenn es der Firma hingegen schlecht geht, ' +
                    'wird der Aktienpreis eher sinken.');
            break;
            case 3:
                alert('Diese Antwort ist leider falsch.\n\n' +
                    'Aus dem Instruktionstext:\n' +
                    'Mit einer Wahrscheinlichkeit von X% wird der Zustand '+
                    'gleich bleiben wie er in der letzten Runde war. Das heisst, das ein guter Zustand ' +
                    'dann in einer Weiteren Runde guten Zustands fortgeführt würde, und ein schlechter ' +
                    'Zustand mit weiterhin schlechtem Zustand. Mit einer Wahrscheinlichkeit von ' +
                    'X% verändert sich jedoch der Zustand vom guten zum schlechten oder umgekehrt.');
            break;
            case 4:
                alert('Diese Antwort ist leider falsch.\n\n' +
                    'Aus dem Instruktionstext:\n' +
                    'Sollte Ihnen die tatsächliche Gewinnwahrscheinlichkeit der Lotterie nicht ausreichen ' +
                    '(die Gewinnwahrscheinlichkeit der Lotterie also kleiner sein als die von Ihnen angegebene ' +
                    'mindest-Gewinnwahrscheinlichkeit), dann wetten Sie automatisch auf den Preisanstieg und ' +
                    'erhalten Bonuspunkte falls dieser eintritt. Sollte die Gewinnwahrscheinlichkeit der ' +
                    'Lotterie aber gleich gross oder sogar grösser sein als die von Ihnen angegebene ' +
                    'mindest-Gewinnwahrscheinlichkeit, dann wird die Lotterie ausgespielt, und Sie erhalten mit ' +
                    'der tatsächlichen Wahrscheinlichkeit der Lotterie die Bonuspunkte.');
            break;
            case 5:
                alert('Diese Antwort ist leider falsch.\n\n' +
                    'Aus dem Instruktionstext:\n' +
                    'Stellen Sie sich vor, dass Sie mit Sicherheit wüssten, dass der Preis ansteigen wird:' +
                    'Die Lotterie müsste ebenfalls eine garantierte Auszahlung bieten (also 100% Gewinnchance),' +
                    'damit Sie nicht eindeutig die Wette bevorzugen.');
            break;
            case 6:
                alert('Diese Antwort ist leider falsch.\n\n' +
                    'Aus dem Instruktionstext:\n' +
                    'Nach der letzten Runde jedes Blocks wird es noch ein letztes Preis-Update geben. ' +
                    'Falls Sie die Aktie in der letzten Runde noch hielten, wird diese nach dem Preis-Update' +
                    'automatisch verkauft, so dass Sie am Ende des Blocks nur noch Bargeld halten.');
            break;

        }
        $$('id_wrong_answers').value = parseInt($$('id_wrong_answers').value) +  1;
    }
};

// Handle the belief slider input:
change_slider_value = function(){
    $$('belief_feedback').innerHTML = $$('belief_slider').value;
    // Reveal the slider handle
    if ($$('belief_slider').classList.contains('slider_hidden')) {
        $$('belief_slider').classList.remove('slider_hidden')
    }
};
