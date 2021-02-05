var add_to_cart_btn = document.getElementsByClassName('add-to-cart')
var update_quantity_btn = document.getElementsByClassName('update-item')
var loading_content_btn = document.getElementsByClassName('loading-content')


var order_item_panels = document.getElementsByClassName('order-item')
var topping_checkbox = document.getElementsByClassName('topping-checkbox')
var scroll_btn = document.getElementById('scroll-btn')
var nav = document.getElementById('sticky-navbar')


var pizza_link = document.getElementById('pizza')
var sub_link = document.getElementById('subs')
var othersub_link = document.getElementById('othersubs')
var pasta_link = document.getElementById('pasta')
var salad_link = document.getElementById('salads')
var dinner_link = document.getElementById('dinners')

var pizza_header = document.getElementById('pizza-header')
var sub_header = document.getElementById('sub-header')
var othersub_header = document.getElementById('othersub-header')
var pasta_header = document.getElementById('pasta-header')
var salad_header = document.getElementById('salad-header')
var dinner_header = document.getElementById('dinner-header')



// Initialize all Bootstrap popover on a page
$(document).ready(function() {
  $('[data-toggle="popover"]').popover()
})


// Show or hide scroll button
window.addEventListener('scroll', function() {

  var windowPosition = window.scrollY

  if(windowPosition >= 400) {
    scroll_btn.style.cssText = "visibility: visible; opacity: 1"
  } else {
    scroll_btn.style.cssText = "visibility: hidden; opacity: 0"
  }
})


// Adding sticky-top class to menu item navbar to set it's position on the top when scrolling page down
window.addEventListener('scroll', function() {

  if(nav !== null) {
    var nav_position = nav.offsetTop;

    if(window.pageYOffset >= nav_position) {
      nav.classList.add('sticky-top')
    } else {
      nav.classList.remove('sticky-top')
    }
  }
})


// Scrolling to specific menu item type
function scrollToElement(element) {
  element.scrollIntoView({behavior: 'smooth', block: 'center'})
}



if(nav !== null) {
  pizza_link.addEventListener('click', function() { scrollToElement(pizza_header) })

  sub_link.addEventListener('click', function() { scrollToElement(sub_header) })

  othersub_link.addEventListener('click', function() { scrollToElement(othersub_header) })

  pasta_link.addEventListener('click', function() { scrollToElement(pasta_header) })

  salad_link.addEventListener('click', function() { scrollToElement(salad_header) })

  dinner_link.addEventListener('click', function() { scrollToElement(dinner_header) })
}


// Scrolling page to top
function scrollPageToTop() {
  window.scroll({
    top: 0,
    behavior: 'smooth'
  })
}



scroll_btn.addEventListener('click', function() {
  scrollPageToTop()
})



// Function to show a loading spinner
function showLoadingSpinner(id) {
  var spinner_id = 'spinner-' + id
  var spinner = document.getElementById(spinner_id)
  spinner.style.display = 'block'
}



// Adding or removing class while clicking specified order item panel
for(i = 0; i < order_item_panels.length; i++) {
  order_item_panels[i].addEventListener('click', function() {

     var item_id = this.dataset.itemId
     var item_type = this.dataset.itemType
     var panel_header_id = item_type + '-' + item_id
     var panel_header = document.getElementById(panel_header_id)

     if(panel_header.classList.contains('panel-header-active')) {
       panel_header.classList.remove('panel-header-active')
     } else {
       for(i = 0; i < order_item_panels.length; i++) {
         order_item_panels[i].classList.remove('panel-header-active')
       }
       panel_header.classList.add('panel-header-active')
     }
  })
}



// Clearing quantity inputs and toppings checkboxes whenever other item order panel is clicked
for(j = 0; j < order_item_panels.length; j++) {
  order_item_panels[j].addEventListener('click', function() {

    var item_type = this.dataset.itemType
    var item_id = this.dataset.itemId

    for(i = 0; i < topping_checkbox.length; i++) {
      if(topping_checkbox[i].checked === true) {
        topping_checkbox[i].checked = false
      }
      topping_checkbox[i].removeAttribute("disabled")
    }
  })
}



// Checking if toppings quantity selected by user is within the general limit of available toppings quantity
var toppings_checked = 0
for(i = 0; i < topping_checkbox.length; i++) {
  topping_checkbox[i].addEventListener('click', function() {

    var toppings_limit = this.dataset.toppingsLimit
    var toppings_counter = 0

    for(j = 0; j < topping_checkbox.length; j++) {
      if(topping_checkbox[j].checked === true) {
        toppings_counter += 1
      }
    }

    toppings_checked = toppings_counter

    if(toppings_checked == toppings_limit) {
      for(k = 0; k < topping_checkbox.length; k++) {
        if(topping_checkbox[k].checked === false) {
          topping_checkbox[k].setAttribute("disabled", "")
        }
      }
    } else if(toppings_checked < toppings_limit) {
        for(l = 0; l < topping_checkbox.length; l++) {
          topping_checkbox[l].removeAttribute("disabled")
        }
    }
  })
}



// Showing a loading spinner while adding item to cart
for(i = 0; i < loading_content_btn.length; i++) {
  loading_content_btn[i].addEventListener('click', function(e) {
    e.preventDefault()

    var item_id = this.dataset.orderItemId

    showLoadingSpinner(item_id)
  })
}



// Sending data to 'addItem' url to add clicked item to shopping cart and receive response
for(i = 0; i < add_to_cart_btn.length; i++) {
  add_to_cart_btn[i].addEventListener('click', function(e) {
    e.preventDefault()

    var item_id = this.dataset.orderItemId
    var item_type = this.dataset.orderItemType
    var action = this.dataset.action

    var selected_toppings = []

    for(i = 0; i < topping_checkbox.length; i++) {
      if(topping_checkbox[i].checked == true) {
        selected_toppings.push(topping_checkbox[i].value)
      }
    }

    var url = '/addItem/'

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({'id': item_id, 'toppings': selected_toppings.join(', '), 'action': action})
    })

    .then((response) => {
      return response.json()
    })

    .then((data) => {
      location.reload()
    })
  })
}


// Sending data to 'updateItem' url to update quantity of specified item in shopping cart and receive response
for(i = 0; i < update_quantity_btn.length; i++) {
  update_quantity_btn[i].addEventListener('click', function(e) {
    e.preventDefault()

    var order_item_id = this.dataset.orderItemId
    var toppings = this.dataset.orderItemToppings
    var action = this.dataset.action

    if(toppings == 'None') {
      toppings = ''
    }

    var url = '/updateItem/'

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({'id': order_item_id, 'toppings': toppings, 'action': action})
    })

    .then((response) => {
      return response.json()
    })

    .then((data) => {
      location.reload()
    })
  })
}
