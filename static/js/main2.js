(function ($) {
	"use strict";

	var $document = $(document),
		$window = $(window),
		$body = $('body'),
		$html = $('html'),
		$ttPageContent = $('#tt-pageContent'),
		$ttFooter = $('#tt-footer'),
		$ttHeader = $('#tt-header'),

		// Template Blocks
		blocks = {
			ttProductMasonry: $ttPageContent.find('.tt-product-listing-masonry'),
			ttLookBookMasonry: $ttPageContent.find('.tt-lookbook-masonry'),
			ttInputCounter: $('.tt-input-counter'),
			modalAddToCart: $('#modalAddToCartProduct'),
			ttMobileProductSlider: $('.tt-mobile-product-slider'),
			ttCountdown: $ttPageContent.find('.tt-countdown'),
			ttBtnAddProduct: $ttPageContent.find('.tt_product_showmore'),
			ttOptionsSwatch: $ttPageContent.find('.tt-options-swatch'),
			ttProductItem: $ttPageContent.find('.tt-product, .tt-product-design02'),
			ttProductDesign02: $ttPageContent.find('.tt-product-design02'),
			ttProductDesign01: $ttPageContent.find('.tt-product'),
			ttLookbook: $ttPageContent.find('.tt-lookbook'),
			ttfooterMobileCollapse: $ttFooter.find('.tt-collapse-title'),
			ttBackToTop: $('#js-back-to-top'),
			ttHeaderDropdown: $ttHeader.find('.tt-dropdown-obj'),
			mobileMenuToggle: $('#js-menu-toggle'),
			ttCarouselProducts: $ttPageContent.find('.tt-carousel-products'),
			sliderRevolution: $ttPageContent.find('.slider-revolution'),
			ttItemsCategories: $ttPageContent.find('.tt-items-categories'),
			ttDotsAbsolute: $ttPageContent.find('.tt-dots-absolute'),
			ttAlignmentImg: $ttPageContent.find('.tt-alignment-img'),
			ttModalQuickView: $('#ModalquickView'),
			ttPromoFixed: $('#js-tt-promo-fixed'),
			jsMobileSlider: $('#js-mobile-slider'),
		};

	var ttwindowWidth = window.innerWidth || $window.width();


	dataBg('#tt-pageContent [data-bg]');

	function dataBg(el) {
		$(el).each(function () {
			var $this = $(this),
				bg = $this.attr('data-bg');
			$this.css({
				'background-image': 'url(' + bg + ')'
			});
		});
	};
	// lookbook.html
	if (blocks.ttLookbook.length) {
		ttLookbook(ttwindowWidth);
	};
	// tt-hotspot
	function ttLookbook(ttwindowWidth) {
		//add lookbook popup
		var objPopup = $('.tt-lookbook-popup');
		if (!objPopup.length) {
			$body.append('<div class="tt-lookbook-popup"><div class="tt-lookbook-container"></div></div>');
		};

		blocks.ttLookbook.on('click', '.tt-hotspot', function (e) {
			var $this = $(this),
				target = e.target,
				ttHotspot = $('.tt-hotspot'),
				ttwindowWidth = window.innerWidth || $window.width(),
				ttCenterBtn = $('.tt-btn').innerHeight() / 2,
				ttWidthPopup = $('.tt-hotspot-content').innerWidth();


			ttwindowWidth <= 789 ? ttLookbookMobile($this) : ttLookbookDesktop($this);

			//ttLookbookDesktop
			function ttLookbookDesktop($this) {

				if ($this.hasClass('active')) return;

				var objTop = $this.offset().top + ttCenterBtn,
					objLeft = $this.offset().left,
					objContent = $this.find('.tt-hotspot-content').detach();

				//check if an open popup
				var checkChildren = $('.tt-lookbook-container').children().size();
				if (checkChildren > 0) {
					if (ttwindowWidth <= 789) {
						closePopupMobile();
					} else {
						closePopupDesctop();
					};
				}

				//open popup
				popupOpenDesktop(objContent, objTop, objLeft);

			};

			function popupOpenDesktop(objContent, objTop, objLeft) {
				//check out viewport(left or right)
				var halfWidth = ttwindowWidth / 2,
					objLeftFinal = 0;

				if (halfWidth < objLeft) {
					objLeftFinal = objLeft - ttWidthPopup - 7;
					popupShowLeft(objLeftFinal);
				} else {
					objLeftFinal = objLeft + 45;
					popupShowRight(objLeftFinal);
				};

				$('.tt-lookbook-popup').find('.tt-lookbook-container').append(objContent);
				$this.addClass('active').siblings().removeClass('active');

				function popupShowLeft(objLeftFinal) {
					$('.tt-lookbook-popup').css({
						'top': objTop,
						'left': objLeftFinal,
						'display': 'block'
					}, 300).animate({
						marginLeft: 26 + 'px',
						opacity: 1
					}, 300);
				};

				function popupShowRight(objLeftFinal) {
					$('.tt-lookbook-popup').css({
						'top': objTop,
						'left': objLeftFinal,
						'display': 'block'
					}).animate({
						marginLeft: -26 + 'px',
						opacity: 1
					});
				};
			};
			//ttLookbookMobile
			function ttLookbookMobile($this) {
				var valueTop = $this.attr('data-top') + '%',
					valueLeft = $this.attr('data-left') + '%';

				$this.find('.tt-btn').css({
					'top': valueTop,
					'left': valueLeft
				});
				$this.css({
					'top': '0px',
					'left': '0px',
					'width': '100%',
					'height': '100%'
				});
				$this.addClass('active').siblings().removeClass('active');
				$this.find('.tt-content-parent').fadeIn(200);
			};
			//Close mobile
			if (ttwindowWidth <= 789) {
				if ($('.tt-btn-close').is(e.target)) {
					closePopupMobile();
					return false;
				};
				if ($('.tt-hotspot').is(e.target)) {
					closePopupMobile();
				};
				$(document).mouseup(function (e) {
					if (!$('.tt-lookbook-popup').is(e.target) && $('.tt-lookbook-popup').has(e.target).length === 0 && !$('.tt-hotspot').is(e.target) && $('.tt-hotspot').has(e.target).length === 0) {
						closePopupDesctop();
					};
				});
			};
			//Close desctope
			if (ttwindowWidth > 789) {
				//ttLookbookClose
				$(document).mouseup(function (e) {
					var ttwindowWidth = window.innerWidth || $window.width();
					if ($('.tt-btn-close').is(e.target)) {
						closePopupDesctop();
						return false;
					};
					if (!$('.tt-lookbook-popup').is(e.target) && $('.tt-lookbook-popup').has(e.target).length === 0 && !$('.tt-hotspot').is(e.target) && $('.tt-hotspot').has(e.target).length === 0) {
						closePopupDesctop();
					};
				});
			};

			function closePopupDesctop() {
				//detach content popup
				var detachContentPopup = $('.tt-lookbook-popup').removeAttr("style").find('.tt-hotspot-content').detach();
				$('.tt-hotspot.active').removeClass('active').find('.tt-content-parent').append(detachContentPopup);
			};

			function closePopupMobile() {
				if ($('.tt-lookbook-container').is(':has(div)')) {
					var checkPopupContent = $('.tt-lookbook-container').find('.tt-hotspot-content').detach();
					$('.tt-hotspot.active').find('.tt-content-parent').append(checkPopupContent);
				};
				$('.tt-lookbook').find('.tt-hotspot.active').each(function (index) {
					var $this = $(this),
						valueTop = $this.attr('data-top') + '%',
						valueLeft = $this.attr('data-left') + '%';

					$this.removeClass('active').removeAttr("style").css({
						'top': valueTop,
						'left': valueLeft,
					}).find('.tt-btn').removeAttr("style").next().removeAttr("style");
				});
			};

			function checkclosePopupMobile() {
				$('.tt-hotspot').find('.tt-content-parent').each(function () {
					var $this = $(this);
					if ($this.css('display') == 'block') {
						var $thisParent = $this.closest('.tt-hotspot'),
							valueTop = $thisParent.attr('data-top') + '%',
							valueLeft = $thisParent.attr('data-left') + '%';

						$this.removeAttr("style").prev().removeAttr("style");
						$thisParent.removeAttr("style").css({
							'top': valueTop,
							'left': valueLeft,
						});
					};
				});
			};
			$(window).resize(debouncer(function (e) {
				var ttwindowWidth = window.innerWidth || $window.width();
				if (ttwindowWidth <= 789) {
					closePopupMobile();
				} else {
					closePopupDesctop();
					checkclosePopupMobile();
				};
			}));
		});
	};
	// Lookbook Masonr
	function gridLookbookMasonr() {
		// init Isotope
		var $grid = blocks.ttLookBookMasonry.find('.tt-lookbook-init').isotope({
			itemSelector: '.element-item',
			layoutMode: 'masonry',
			gutter: 0
		});
		// layout Isotope after each image loads
		$grid.imagesLoaded().progress(function () {
			$grid.addClass('tt-show').isotope('layout');
		});
		//add item
		var isotopShowmoreJs = $('.isotop_showmore_js .btn'),
			ttAddItem = $('.tt-add-item');
		if (isotopShowmoreJs.length && ttAddItem.length) {
			isotopShowmoreJs.on('click', function (e) {
				e.preventDefault();
				$.ajax({
					url: 'ajax_post.php',
					success: function (data) {
						var $item = $(data);
						ttAddItem.append($item);
						$grid.isotope('appended', $item);
						adjustOffset();
					}
				});

				function adjustOffset() {
					var offsetLastItem = ttAddItem.children().last().children().offset().top - 180;
					$($body, $html).animate({
						scrollTop: offsetLastItem
					}, 500);
				};
				return false;
			});
		};
	};
})(jQuery);