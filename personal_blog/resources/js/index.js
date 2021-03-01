$(document).ready(function ($) {
    let animationDelay = 2500,
        barAnimationDelay = 3800,
        barWaiting = barAnimationDelay - 3000,
        lettersDelay = 50,
        typeLettersDelay = 150,
        selectionDuration = 500,
        typeAnimationDelay = selectionDuration + 800,
        revealDuration = 600,
        revealAnimationDelay = 1500;

    initHeadline();

    function initHeadline() {
        singleLetters($('.cd-headline.letters').find('b'));
        animateHeadline($('.cd-headline'));
    }

    function singleLetters($words) {
        $words.each(function () {
            let word = $(this),
                letters = word.text().split(''),
                selected = word.hasClass('is-visible');
            for (let i in letters) {
                if (word.parents('.rotate-2').length > 0) letters[i] = '<em>' + letters[i] + '</em>';
                letters[i] = (selected) ? '<i class="in">' + letters[i] + '</i>' : '<i>' + letters[i] + '</i>';
            }
            let newLetters = letters.join('');
            word.html(newLetters).css('opacity', 1);
        });
    }

    function animateHeadline($headlines) {
        let duration = animationDelay;
        $headlines.each(function () {
            let headline = $(this);

            if (headline.hasClass('loading-bar')) {
                duration = barAnimationDelay;
                setTimeout(function () {
                    headline.find('.cd-words-wrapper').addClass('is-loading')
                }, barWaiting);
            } else if (headline.hasClass('clip')) {
                let spanWrapper = headline.find('.cd-words-wrapper'),
                    newWidth = spanWrapper.width() + 10;
                spanWrapper.css('width', newWidth);
            } else if (!headline.hasClass('type')) {
                let words = headline.find('.cd-words-wrapper b'),
                    width = 0;
                words.each(function () {
                    let wordWidth = $(this).width();
                    if (wordWidth > width) width = wordWidth;
                });
                headline.find('.cd-words-wrapper').css('width', width);
            }
            setTimeout(function () {
                hideWord(headline.find('.is-visible').eq(0))
            }, duration);
        });
    }

    function hideWord($word) {
        let nextWord = takeNext($word);

        if ($word.parents('.cd-headline').hasClass('type')) {
            let parentSpan = $word.parent('.cd-words-wrapper');
            parentSpan.addClass('selected').removeClass('waiting');
            setTimeout(function () {
                parentSpan.removeClass('selected');
                $word.removeClass('is-visible').addClass('is-hidden').children('i').removeClass('in').addClass('out');
            }, selectionDuration);
            setTimeout(function () {
                showWord(nextWord, typeLettersDelay)
            }, typeAnimationDelay);

        } else if ($word.parents('.cd-headline').hasClass('letters')) {
            let bool = ($word.children('i').length >= nextWord.children('i').length);
            hideLetter($word.find('i').eq(0), $word, bool, lettersDelay);
            showLetter(nextWord.find('i').eq(0), nextWord, bool, lettersDelay);

        } else if ($word.parents('.cd-headline').hasClass('clip')) {
            $word.parents('.cd-words-wrapper').animate({width: '2px'}, revealDuration, function () {
                switchWord($word, nextWord);
                showWord(nextWord);
            });

        } else if ($word.parents('.cd-headline').hasClass('loading-bar')) {
            $word.parents('.cd-words-wrapper').removeClass('is-loading');
            switchWord($word, nextWord);
            setTimeout(function () {
                hideWord(nextWord)
            }, barAnimationDelay);
            setTimeout(function () {
                $word.parents('.cd-words-wrapper').addClass('is-loading')
            }, barWaiting);

        } else {
            switchWord($word, nextWord);
            setTimeout(function () {
                hideWord(nextWord)
            }, animationDelay);
        }
    }

    function showWord($word, $duration) {
        if ($word.parents('.cd-headline').hasClass('type')) {
            showLetter($word.find('i').eq(0), $word, false, $duration);
            $word.addClass('is-visible').removeClass('is-hidden');

        } else if ($word.parents('.cd-headline').hasClass('clip')) {
            $word.parents('.cd-words-wrapper').animate({'width': $word.width() + 10}, revealDuration, function () {
                setTimeout(function () {
                    hideWord($word)
                }, revealAnimationDelay);
            });
        }
    }

    function hideLetter($letter, $word, $bool, $duration) {
        $letter.removeClass('in').addClass('out');

        if (!$letter.is(':last-child')) {
            setTimeout(function () {
                hideLetter($letter.next(), $word, $bool, $duration);
            }, $duration);
        } else if ($bool) {
            setTimeout(function () {
                hideWord(takeNext($word))
            }, animationDelay);
        }

        if ($letter.is(':last-child') && $('html').hasClass('no-csstransitions')) {
            let nextWord = takeNext($word);
            switchWord($word, nextWord);
        }
    }

    function showLetter($letter, $word, $bool, $duration) {
        $letter.addClass('in').removeClass('out');

        if (!$letter.is(':last-child')) {
            setTimeout(function () {
                showLetter($letter.next(), $word, $bool, $duration);
            }, $duration);
        } else {
            if ($word.parents('.cd-headline').hasClass('type')) {
                setTimeout(function () {
                    $word.parents('.cd-words-wrapper').addClass('waiting');
                }, 200);
            }
            if (!$bool) {
                setTimeout(function () {
                    hideWord($word)
                }, animationDelay)
            }
        }
    }

    function takeNext($word) {
        return (!$word.is(':last-child')) ? $word.next() : $word.parent().children().eq(0);
    }

    function switchWord($oldWord, $newWord) {
        $oldWord.removeClass('is-visible').addClass('is-hidden');
        $newWord.removeClass('is-hidden').addClass('is-visible');
    }
});

function sendContactEmail(element) {
    let contactEmail = $.trim($("#contactEmail").val());
    if (contactEmail.match(/.+@.+\..+/)) {
        changeButtonState(element, "sending");
        $("#contactEmail").attr("disabled", true);
        let contactName = $.trim($("#contactName").val());
        let contactMessage = $.trim($("#contactMessage").val());

        let param = "email=" + contactEmail;
        param += "&name=" + contactName;
        param += "&message=" + contactMessage;
        $.post('/contact', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                changeButtonState(element, "tick");
                $("#contactName").val("");
                $("#contactEmail").val("");
                $("#contactMessage").val("");
            }else{
                changeButtonState(element,"retry");
                $("#registerEmail").attr("disabled", false);
            }
        })
    } else {
        alert("Fail (Front) : Invalid email");
        return false;
    }
}

