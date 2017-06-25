
// making navbar active
$('ul.nav li.dropdown').hover(function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
}, function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
});

// calender 

// This string holds the dates that have events
	var eventsString = [
		'11/17/2014',
		'11/18/2014',
		'11/2/2014',
		'12/14/2014',
		'1/6/2015',
		'1/8/2015'
	];

function highlightDays(date) {
    for (var i = 0; i < eventsString.length; i++) {
        if (new Date(eventsString[i]).toString() == date.toString()) {
            return [true, 'dayWithEvents'];
        }
    }
    return [true, ''];

}

$('#calendar').datepicker({
        inline: true,
        showOtherMonths: true,
        dayNamesMin: ['SUN', 'MON', 'TUE', 'WED', 'ThU', 'FRI', 'SAT'],
        beforeShowDay: highlightDays
    });


var $calendarADate = $( "#calendarADate" );
var $calendarA = $( "#calendarA" );
var dateFormat = 'MMMM DD, YYYY';

function displayDate( date ){

    var mDate = moment( date );
    var month = mDate.format( 'MMMM' );
    var day = mDate.format( 'DD' );
    var year = mDate.format( 'YYYY' );

    var template = '<div class="month-section"><div class="month">' + month + '</div></div><div class="date-year"><div class="year">' + year + '</div><div class="day">' + day + '</div></div>';
    $calendarADate.html( template );

}

    $calendarA.datepicker({
        inline: true,
        showOtherMonths: true,
        dayNamesMin: ['SUN', 'MON', 'TUE', 'WED', 'ThU', 'FRI', 'SAT'],
		beforeShowDay: highlightDays,
        onSelect: function( date ){

            displayDate( date );

        }
    });

    var currentDate = $calendarA.datepicker( 'getDate' );
    displayDate( currentDate );


$(document).ready(function(){
 
	function eventInit(){
		$('.ui-datepicker-calendar tbody tr td').click(function(){
			if($(this).hasClass('dayWithEvents')){
				$('.list-of-events').fadeIn('nornal');
				$('.no-events').fadeOut(1);
				eventInit();
			}else{
				$('.no-events').fadeIn('nornal');
				$('.list-of-events').fadeOut(1);
				eventInit();
			}
		});
		
		
	}
	eventInit();
    $('.topmenu > li').click(function(){
       $('.topmenu li').removeClass('active');
       $(this).addClass('active'); 
    });
    
    $('.closeButton').click(function(){
        $('.topmenu li').removeClass('active');
    });
    
    function nextPrevInit(){
    $('.ui-datepicker-next, .ui-datepicker-prev').click(function(){
		eventInit();
    });	
}
nextPrevInit();
    
});

// calender 

// This string holds the dates that have events
    var eventsString = [
        '11/17/2014',
        '11/18/2014',
        '11/2/2014',
        '12/14/2014',
        '1/6/2015',
        '1/8/2015'
    ];

function highlightDays(date) {
    for (var i = 0; i < eventsString.length; i++) {
        if (new Date(eventsString[i]).toString() == date.toString()) {
            return [true, 'dayWithEvents'];
        }
    }
    return [true, ''];

}

// top menu toggle

var $topMenu = $( '.topmenu' );
var $topMenuList = $( ' > li', $topMenu );
var $topMenuDropdownButtons = $( ' > a', $topMenuList );
var $topMenuDropdowns = $( ' > .toggle-section', $topMenuList );
var $topMenuDropdownCloseButtons = $( '.closeButton', $topMenuDropdowns );

$( 'body' ).click( function(){

    $topMenuDropdowns.slideUp( 200 );
    $('.topmenu li').removeClass('active');

} );

$topMenu.click( function( e ){

    e.stopPropagation();

} );

$topMenuDropdownCloseButtons.click( function( e ){

    e.preventDefault();
    $('.topmenu li').removeClass('active');
    $( this ).closest( '.toggle-section' ).slideUp( 200 , function(){
        $('.topmenu li').removeClass('active');
    });

} );

$topMenuDropdownButtons.click( function( e ){

    e.preventDefault();
    
    var $dropdown = $( this ).siblings( '.toggle-section' );
    $topMenuDropdowns.slideUp( 200 );
    $dropdown.slideDown( 200 );

} );


// video player




$(function() {
    var Accordion = function(el, multiple) {
        this.el = el || {};
        this.multiple = multiple || false;

        // Variables privadas
        var links = this.el.find('.link');
        // Evento
        links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
    }

    Accordion.prototype.dropdown = function(e) {
        var $el = e.data.el;
            $this = $(this),
            $next = $this.next();

        $next.slideToggle();
        $this.parent().toggleClass('open');

        if (!e.data.multiple) {
            $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
        };
    }   

    var accordion = new Accordion($('.accordion'), false);
});







