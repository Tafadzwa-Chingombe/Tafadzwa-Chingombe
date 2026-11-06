// which frame this page is drawn in: L 16:9, P 9:16, S 4:5 (set before the page lays out)
(function () { var w = innerWidth, h = innerHeight; document.documentElement.className = w > h ? 'L' : (h / w > 1.5 ? 'P' : 'S'); })();
