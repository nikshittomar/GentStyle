$(document).ready(function() {
 

console.log('hello')


  // Only for desktop view
  if (window.innerWidth >= 992) {
    const navbar = document.querySelector('.wrap-menu-desktop');

    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {   // scroll threshold
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }


  // Newsletter subscription
  const newsletterForm = document.getElementById('newsletterForm');
  newsletterForm.addEventListener('submit', function(e){
    e.preventDefault();
    const email = this.email.value;
    if(email) {
      alert(`Thank you for subscribing with ${email}!`);
      this.reset();
    }
  });



  // Toggle Mobile Menu
  const menuBtn = document.querySelector('.btn-show-menu-mobile');
  const mobileMenu = document.querySelector('.menu-mobile');

  menuBtn.addEventListener('click', () => {
    mobileMenu.style.display = mobileMenu.style.display === 'block' ? 'none' : 'block';
  });


   const slides = document.querySelectorAll(".slide");
  const prevBtn = document.querySelector(".prev");
  const nextBtn = document.querySelector(".next");
  let index = 0;

  function showSlide(i) {
    slides.forEach((slide, idx) => {
      slide.classList.remove("active");
      if (idx === i) slide.classList.add("active");
    });
  }

  prevBtn.addEventListener("click", () => {
    index = (index - 1 + slides.length) % slides.length;
    showSlide(index);
  });

  nextBtn.addEventListener("click", () => {
    index = (index + 1) % slides.length;
    showSlide(index);
  });

  // Auto slide every 5 sec
  setInterval(() => {
    index = (index + 1) % slides.length;
    showSlide(index);
  }, 5000);

   // Contact form submit
    document.getElementById('contactForm').addEventListener('submit', function(e) {
      e.preventDefault();
      alert('Thank you for contacting us!');
      this.reset();
    });

    // Simple Google Map placeholder
    function initMap() {
      const mapOptions = {
        center: { lat: 40.691446, lng: -73.886787 },
        zoom: 11
      };
      const map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
      new google.maps.Marker({
        position: mapOptions.center,
        map: map,
        title: 'Coza Store Center'
      });
    }


    const filterButtons = document.querySelectorAll(".filter-buttons button");
    const products = document.querySelectorAll(".product");

    filterButtons.forEach(button => {
      button.addEventListener("click", () => {
        document.querySelector(".filter-buttons .active").classList.remove("active");
        button.classList.add("active");

        const filter = button.getAttribute("data-filter");
        products.forEach(product => {
          if (filter === "all" || product.classList.contains(filter)) {
            product.style.display = "block";
          } else {
            product.style.display = "none";
          }
        });
      });
    });

    // Search toggle
    const toggleSearch = document.querySelector(".toggle-search");
    const searchBar = document.querySelector(".search-bar");
    toggleSearch.addEventListener("click", () => {
      searchBar.style.display = searchBar.style.display === "block" ? "none" : "block";
    });

    // Search filter
    document.getElementById("searchInput").addEventListener("keyup", function () {
      const searchText = this.value.toLowerCase();
      products.forEach(product => {
        const text = product.textContent.toLowerCase();
        product.style.display = text.includes(searchText) ? "block" : "none";
      });
    });

    
  });

  const filterBtn = document.querySelector(".filter-btn");
  const sidebar = document.querySelector(".shop-sidebar");
  const overlay = document.querySelector(".overlay");

  filterBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
  });

  overlay.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
  });

  
  
  document.querySelectorAll('.dropdown-header').forEach(header => {
    header.addEventListener('click', e => {
      e.preventDefault();
      const parent = header.parentElement;
      parent.classList.toggle('active');

      // Close others
      document.querySelectorAll('.dropdown').forEach(item => {
        if (item !== parent) item.classList.remove('active');
        
      });
    });
  });
