import html
import re
import urllib.request
from datetime import date
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter

NOTEBOOK = "projekt_mini.ipynb"
WYJSCIE = Path("docs/index.html")
TYTUL = "Od czego zależą zarobki programistów?"
PODTYTUL = "Analiza ankiety Stack Overflow Developer Survey 2018"
AUTOR = "Olga Dawidowicz"
SLOWA = "zarobki programistów, Stack Overflow, regresja liniowa, braki danych, imputacja KNN, zadowolenie z pracy"
STRESZCZENIE = (
    "Analiza odpowiedzi z ankiety Stack Overflow z 2018 roku, w której uczestniczyło 43 673 respondentów, "
    "Projekt odpowiada na 3 pytania badawcze: co mocniej różnicuje zarobki (kraj czy "
    "staż), czy studia informatyczne wiążą się z wyższą pensją oraz czy zadowolenie z pracy rośnie z "
    "doświadczeniem. Sam kraj wyjaśnia około połowy zmienności zarobków, a sam staż około 19%. Przy tym "
    "samym kraju rok stażu to średnio 3,7% więcej. Luka między informatykami a osobami po innych "
    "kierunkach (około 19,5%) po uwzględnieniu kraju spada do około 5%. Zadowolenie rośnie ze stażem tylko "
    "nieznacznie."
)

# 1) notebook -> sam tekst i wyniki (bez kodu, numerków i ostrzeżeń)
nb = nbformat.read(NOTEBOOK, as_version=4)
for c in nb.cells:
    if c.cell_type == "code":
        c.outputs = [o for o in c.outputs if not (o.output_type == "stream" and o.get("name") == "stderr")]

eksporter = HTMLExporter(template_name="basic", exclude_input=True,
                         exclude_input_prompt=True, exclude_output_prompt=True)
tresc, _ = eksporter.from_notebook_node(nb)
tresc = re.sub(r"<h1.*?</h1>", "", tresc, count=1, flags=re.S)           # pierwszy h1 idzie do nagłówka
tresc = re.sub(r"\n(?:Name: [^\n<]*, )?dtype: [^\n<]*", "", tresc)       # usuwa "Name: ..., dtype: ..."

# 2) motyw cosmo wklejony do pliku
CSS_URL = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cosmo/bootstrap.min.css"
try:
    bootstrap = "<style>" + urllib.request.urlopen(CSS_URL, timeout=15).read().decode("utf-8") + "</style>"
except Exception:
    bootstrap = f'<link rel="stylesheet" href="{CSS_URL}">'

STRONA = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TYTUL%%</title>
%%BOOTSTRAP%%
<style>
:root { --so: #F48024; --so-ciemny: #d9701a; --so-jasny: #fdf1e6; --so-naglowek: #fbd9b8; --ciemny: #232629; }
html { scroll-behavior: smooth; scroll-padding-top: 20px; }
body { background: #fff; color: var(--ciemny); font-size: 1.05rem; line-height: 1.65; }
h1, h2, h3 { font-family: "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif; }

/* menu po lewej */
#sidebar { position: fixed; top: 0; left: 0; bottom: 0; width: 300px; background: #fff;
  border-right: 1px solid #e3e3e3; overflow-y: auto; padding: 70px 1rem 2rem; z-index: 900;
  transition: transform .25s ease; }
#sidebar.hidden { transform: translateX(-100%); }
#sidebar .naglowek { font-size: .75rem; letter-spacing: .08em; text-transform: uppercase; color: #888; margin-bottom: .6rem; }
#sidebar ul { list-style: none; padding-left: 0; margin: 0; }
#sidebar ul ul { padding-left: 1.1rem; }
#sidebar li { position: relative; margin: .15rem 0; }
#sidebar li.collapsed > ul { display: none; }
#sidebar a { display: block; padding: .25rem .5rem .25rem 1.1rem; color: #3b4045; text-decoration: none;
  border-left: 3px solid transparent; font-size: .95rem; border-radius: 3px; }
#sidebar a:hover { background: var(--so-jasny); }
#sidebar a.active { border-left-color: var(--so); background: var(--so-jasny); font-weight: 600; color: #000; }
.toc-arrow { position: absolute; left: -2px; top: .3rem; width: 1rem; font-size: .6rem; color: #999; cursor: pointer; user-select: none; }

/* przycisk menu */
.toggle-sidebar-btn { position: fixed; top: 14px; left: 14px; z-index: 999 !important; width: 42px; height: 42px;
  border: 2px solid var(--ciemny); border-radius: 6px; background: #fff; color: var(--ciemny);
  font-size: 1.3rem; line-height: 1; cursor: pointer; }
.toggle-sidebar-btn:hover { border-color: var(--so); color: var(--so); }

/* układ */
#wrap { margin-left: 300px; transition: margin .25s ease; }
body.full-width #wrap { margin-left: 0; }
main { max-width: 900px; margin: 0 auto; padding: 2.5rem 1.5rem 5rem; }

/* tytuł: pomarańczowy tekst, bez ramki */
.tytul { text-align: center; }
.tytul h1 { font-weight: 700; font-size: 2.6rem; line-height: 1.2; margin: 1rem 0 .4rem; color: var(--so); }
.tytul .pod { font-family: "Palatino Linotype", Palatino, Georgia, serif; font-size: 1.3rem; color: var(--so-ciemny); }
.tytul .linia { height: 4px; background: var(--so); margin: 1rem 0 .7rem; }
.tytul .meta { display: flex; justify-content: space-between; font-size: 1.05rem; color: #444; }
.abstrakt { border-top: 1px solid #ccc; border-bottom: 1px solid #ccc; margin: 1.2rem 0 0; padding: .9rem 0; font-size: .98rem; }
.abstrakt + .abstrakt { border-top: none; margin-top: 0; }
.abstrakt p { margin: 0; }

/* sekcje: baner w kolorze Stack Overflow */
main h1.baner, main h2.baner { background: var(--so); color: #fff; text-align: center; font-weight: 700;
  font-size: 1.7rem; padding: .7rem 1rem; margin: 3.5rem 0 1.5rem; border: none; border-radius: 12px;
  box-shadow: 0 3px 8px rgba(0,0,0,.18); }
main h2:not(.baner), main h3 { margin-top: 2.4rem; font-size: 1.5rem; color: var(--so); font-weight: 700; }
main hr { margin: 2rem 0 0; opacity: .15; }
.anchor-link { display: none; }
main img { display: block; max-width: 100%; height: auto; margin: 1.2rem auto; }

/* wydruki tekstowe */
main pre { background: none !important; border: none !important; padding: 0 !important; margin: .5rem 0;
  font-family: inherit; font-size: 1rem; color: inherit; white-space: pre-wrap; }
main code { color: #b4510a; background: #f6f1ec; padding: .1rem .3rem; border-radius: 3px; }
main blockquote { border-left: 4px solid var(--so); background: #fff8f1; padding: .6rem 1rem; margin: 1rem 0; }

/* tabele: jasnopomarańczowy nagłówek, paski, wyśrodkowane; małe obok siebie */
.tab-row { display: flex; flex-wrap: wrap; justify-content: center; align-items: flex-start; gap: 1.5rem; margin: 1.2rem 0; }
.tab-wrap { overflow-x: auto; margin: 1.2rem 0; }
.tab-row .tab-wrap { margin: 0; }
main table { border-collapse: collapse !important; border: none !important; margin: 0 auto !important;
  width: auto !important; font-size: .95rem; box-shadow: 0 1px 6px rgba(0,0,0,.12); }
main table th, main table td { text-align: center !important; padding: .55rem 1rem !important;
  border: none !important; vertical-align: middle; }
main table thead th { background: var(--so-naglowek) !important; color: #5a2d05 !important; font-weight: 700;
  font-size: 1.08rem; border-bottom: 2px solid var(--so) !important; }
main table tbody tr:nth-child(even) { background: #f7f7f7; }
main table tbody tr:hover { background: var(--so-jasny); }
main table tbody th { text-align: left !important; background: var(--so-jasny) !important; color: #8a4a0f; font-weight: 600; }
@media (max-width: 991px) { #wrap { margin-left: 0; } }
/* Tło kontener na canvas Three.js */
.tlo {
  position: fixed;
  top: -10vh;
  right: -4vw;
  height: 120vh;
  width: 45vw; /* Trochę szersze, by objąć całą spiralę */
  z-index: -1 !important;
  pointer-events: none;
  opacity: 0.16;
}
.tlo canvas { 
  width: 100% !important; 
  height: 100% !important; 
  outline: none; 
}
body.dark .tlo { opacity: 0.28; }
@media (max-width: 991px) { .tlo { opacity: 0.08; width: 60vw; } }

/* wykresy mniejsze */
main img { max-width: 78%; }

/* mniejsze marginesy i czcionka w tabelach */
main table th, main table td { padding: .3rem .65rem !important; }
main table tbody th { padding: .3rem .65rem !important; }

/* szeroka tabela (np. podgląd danych): mniejsza czcionka, kolumny z tekstem szersze */
main table.szeroka { font-size: .88rem; table-layout: fixed; width: 100% !important; }
main table.szeroka th, main table.szeroka td { padding: .25rem .5rem !important; line-height: 1.3; }
main table.szeroka td.dluga { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; cursor: help; }
main table.szeroka td.dluga:hover { white-space: normal; overflow: visible; background: #fff3e6 !important;
  position: relative; z-index: 5; box-shadow: 0 2px 8px rgba(0,0,0,.25); }
main table.szeroka td.waska, main table.szeroka th.waska { width: 70px; }

/* dane pod tabelą jako kafelki */
.kafle { display: flex; flex-wrap: wrap; justify-content: center; gap: .8rem; margin: 1.2rem 0; }
.kafel { background: #fff; border: 1px solid rgba(244,128,36,.55); border-radius: 0px;
  padding: .55rem 1.1rem; min-width: 160px; text-align: center; }
.kafel b { display: block; font-size: 1.45rem; color: #c25e0c; }
.kafel span { font-size: .85rem; color: #555; }
body.dark .kafel { background: #232629; border-color: rgba(244,128,36,.6); }
body.dark .kafel span { color: #bbb; }
main table.szeroka thead th { white-space: normal; word-break: normal; line-height: 1.2; vertical-align: bottom; }
/* opisy "komentarz" / "Odpowiedź" w rozwijanym boxie */
details.odp { margin: .8rem 0 1.4rem; }
details.odp > summary { display: inline-block; cursor: pointer; list-style: none; background: var(--so); color: #fff;
  font-weight: 600; font-size: .9rem; padding: .25rem .9rem; border-radius: 0px; user-select: none; }
details.odp > summary::-webkit-details-marker { display: none; }
details.odp > summary::before { content: "▸ "; }
details.odp[open] > summary::before { content: "▾ "; }
details.odp > summary:hover { background: var(--so-ciemny); }
details.odp .odp-tresc { margin-top: .5rem; padding: .7rem 1rem; background: rgba(244,128,36,.07);
  border: none; border-radius: 0px; }
details.odp .odp-tresc > :last-child { margin-bottom: 0; }

/* wykresy plotly na pełną szerokość */
main .plotly-graph-div { width: 100% !important; max-width: 100%; margin: 1.2rem auto; }
/* Usuwamy zewnętrzne pudełko z Plotly */
body.dark main .plotly-graph-div { background: transparent !important; border-radius: 0; padding: 0; }

/* Wymuszamy szary kolor właściwego tła wewnątrz wykresu Plotly (papier i obszar rysowania) */
body.dark main .plotly-graph-div .bg,
body.dark main .plotly-graph-div .bglayer > rect { fill: #e0e0e0 !important; }
/* przycisk dzień/noc - naprawiony i wyciągnięty na wierzch */
.theme-btn { position: fixed; top: 14px; right: 14px; z-index: 9999 !important; width: 42px; height: 42px;
  border: 1px solid #ccc; border-radius: 50%; background: #fff; color: var(--ciemny);
  font-size: 1.15rem; line-height: 1; cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.15); }
.theme-btn:hover { border-color: var(--so); }

/* tryb ciemny */
body.dark { background: #1b1d1f; color: #e3e3e3; }
body.dark .tytul .meta { color: #bbb; }
body.dark .abstrakt { border-color: #444; }
body.dark #sidebar { background: #232629; border-right-color: #3a3d40; }
body.dark #sidebar a { color: #cfcfcf; }
body.dark #sidebar a:hover, body.dark #sidebar a.active { background: #34302c; color: #fff; }
body.dark .toggle-sidebar-btn, body.dark .theme-btn { background: #232629; color: #e3e3e3; border-color: #555; }
body.dark main h2:not(.baner), body.dark main h3 { color: var(--so); }
body.dark main code { background: #34302c; color: #f5a25d; }
body.dark main blockquote { background: #2a2623; }
body.dark main table { box-shadow: 0 1px 6px rgba(0,0,0,.5); color: #e3e3e3; }
body.dark main table tbody tr:nth-child(even) { background: #2a2d30; }
body.dark main table tbody tr:nth-child(odd) { background: #232629; }
body.dark main table tbody tr:hover { background: #3a332c; }
body.dark main table tbody th { background: #34302c !important; color: #f5a25d; }
body.dark main img { background: #e0e0e0 !important; border-radius: 0; padding: 0; }
@media print { #sidebar, .toggle-sidebar-btn, .theme-btn { display: none; } #wrap { margin: 0; } }
</style>
</head>
<body>
<nav id="sidebar"><div class="naglowek">Spis treści</div></nav>
<button class="toggle-sidebar-btn" id="btn" title="Menu">←</button>
<button class="theme-btn" id="theme" title="Tryb dzień/noc">☾</button>
<div class="tlo" id="tlo"></div>

<div id="wrap">
  <main>
    <header class="tytul">
      <h1>%%TYTUL%%</h1>
      <div class="pod">%%PODTYTUL%%</div>
      <div class="linia"></div>
      <div class="meta"><span>%%DATA%%</span><span>%%AUTOR%%</span></div>
    </header>
    <div class="abstrakt"><p><strong>Streszczenie.</strong> %%STRESZCZENIE%%</p></div>
    <div class="abstrakt"><p><strong>Słowa kluczowe:</strong> <em>%%SLOWA%%</em></p></div>
%%TRESC%%
  </main>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var sidebar = document.getElementById("sidebar");
  var main = document.querySelector("main");
  var DUZE = ["wprowadzenie", "1. porządkowanie i czyszczenie danych", "2. wizualizacje", "3. analiza opisowa", "wnioski",];

  main.querySelectorAll("h1, h2").forEach(function (h) {
    var t = h.textContent.replace("¶", "").trim().toLowerCase();
    if (DUZE.indexOf(t) >= 0 || /^etap \d/.test(t)) h.classList.add("baner");
  });
  var heads = Array.prototype.slice.call(main.querySelectorAll("h1, h2"));

  // spis treści
  var root = document.createElement("ul");
  var stack = [{ level: 0, ul: root, li: null }];
  heads.forEach(function (h, i) {
    if (!h.id) h.id = "sek-" + i;
    var lvl = (h.tagName === "H1" || h.classList.contains("baner")) ? 1 : 2;
    while (stack.length > 1 && stack[stack.length - 1].level >= lvl) stack.pop();
    var parent = stack[stack.length - 1];

    if (parent.li && !parent.ul.parentNode) {
      parent.li.appendChild(parent.ul);
      var arrow = document.createElement("span");
      arrow.className = "toc-arrow";
      arrow.textContent = "▼";
      parent.li.insertBefore(arrow, parent.li.firstChild);
      arrow.addEventListener("click", function (e) {
        e.stopPropagation();
        var li = e.target.parentNode;
        li.classList.toggle("collapsed");
        e.target.textContent = li.classList.contains("collapsed") ? "▶" : "▼";
      });
    }
    var li = document.createElement("li");
    var a = document.createElement("a");
    a.href = "#" + h.id;
    a.textContent = h.textContent.replace("¶", "").trim();
    li.appendChild(a);
    parent.ul.appendChild(li);
    stack.push({ level: lvl, ul: document.createElement("ul"), li: li });
  });
  sidebar.appendChild(root);

  // przycisk menu (strzałka)
  var btn = document.getElementById("btn");
  function ustaw() { btn.textContent = sidebar.classList.contains("hidden") ? "→" : "←"; }
  if (window.innerWidth < 992) { sidebar.classList.add("hidden"); document.body.classList.add("full-width"); }
  ustaw();
  btn.addEventListener("click", function () {
    sidebar.classList.toggle("hidden");
    document.body.classList.toggle("full-width");
    ustaw();
  });

  // podświetlanie bieżącej sekcji
  var links = Array.prototype.slice.call(sidebar.querySelectorAll("a"));
  function spy() {
    var cur = null;
    heads.forEach(function (h) { if (h.getBoundingClientRect().top < 140) cur = h.id; });
    links.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + cur); });
  }
  window.addEventListener("scroll", spy); spy();

// tło: idealny stos klocków 3D za pomocą Three.js (wersja ostateczna - większa i skręcona)
  (function () {
    var script = document.createElement('script');
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
    script.onload = function() {
        var container = document.getElementById("tlo");
        var width = container.clientWidth || window.innerWidth * 0.45;
        var height = container.clientHeight || window.innerHeight * 1.2;

        var scene = new THREE.Scene();
        
        // ZBLIŻONO KAMERĘ: (32, 35, 42) zamiast (40, 40, 50) - co powiększa całą grafikę
        var camera = new THREE.PerspectiveCamera(40, width / height, 1, 1000);
        camera.position.set(50, 50, 60); 
        camera.lookAt(0, 22, 0);

        var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(width, height);
        container.appendChild(renderer.domElement);

        var ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
        scene.add(ambientLight);
        var dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
        dirLight.position.set(20, 40, 30);
        scene.add(dirLight);
      // obrócenie sceny o 12 stopni w lewo, by wieża była lekko pochylona
        var tower = new THREE.Group();
        scene.add(tower);

        // DELIKATNIE POWIĘKSZONE KLOCKI, by po skręceniu nadal wyglądały masywnie
        var geometry = new THREE.BoxGeometry(18, 2.6, 7);
        
        var materials = [
            new THREE.MeshLambertMaterial({ color: 0xFF6600 }), // Prawy (Pomarańczowy)
            new THREE.MeshLambertMaterial({ color: 0x6575EA }), // Lewy (Niebieski)
            new THREE.MeshLambertMaterial({ color: 0xC4CBE1 }), // Góra (Jasny)
            new THREE.MeshLambertMaterial({ color: 0x6575EA }), // Dół
            new THREE.MeshLambertMaterial({ color: 0x6575EA }), // Przód
            new THREE.MeshLambertMaterial({ color: 0xFF6600 }), // Tył
        ];

        // NOWE USTAWIENIA MATEMATYCZNE - WIĘKSZY SKRĘT
        const count = 25; // Lekko więcej klocków, by wieża nadal wypełniała ekran po zbliżeniu
        const heightStep = 2.6; // Odstęp równy wysokości klocka
        const angleStep = 0.28; // ZWIĘKSZONY SKRĘT (z 0.15 na 0.28)

        for (let i = 0; i < count; i++) {
            const mesh = new THREE.Mesh(geometry, materials);
            
            mesh.position.x = 0;
            mesh.position.z = 0;
            mesh.position.y = i * heightStep;
            
            // Mocniejszy obrót każdego klocka
            mesh.rotation.y = i * angleStep;
            
            // Krawędzie
            var edges = new THREE.EdgesGeometry(geometry);
            var line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.15 }));
            mesh.add(line);
            
            tower.add(mesh);
        }

        // Pochylenie CAŁEJ wieży o 12 stopni
        scene.rotation.z = -12 * Math.PI / 180;
        
        // Obniżenie wieży, żeby była wyśrodkowana
        scene.position.y = -12;

        var zegar = new THREE.Clock();
        var PREDKOSC = 0.15;   // radiany na sekundę: 0.15 to pełny obrót w ok. 42 s
        var bezRuchu = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        function animate() {
            requestAnimationFrame(animate);
            if (!bezRuchu) tower.rotation.y = zegar.getElapsedTime() * PREDKOSC;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', function() {
            var newW = container.clientWidth || window.innerWidth * 0.45;
            var newH = container.clientHeight || window.innerHeight * 1.2;
            camera.aspect = newW / newH;
            camera.updateProjectionMatrix();
            renderer.setSize(newW, newH);
        });
    };
    document.head.appendChild(script);
  })();

  // tryb dzień/noc
  var tbtn = document.getElementById("theme");
  var zapisany = null;
  try { zapisany = localStorage.getItem("tryb"); } catch (e) {}
  var ciemny = zapisany ? zapisany === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
  function motyw() {
    document.body.classList.toggle("dark", ciemny);
    tbtn.textContent = ciemny ? "🌙" : "☀";
  }
  motyw();
  tbtn.addEventListener("click", function () {
    ciemny = !ciemny;
    try { localStorage.setItem("tryb", ciemny ? "dark" : "light"); } catch (e) {}
    motyw();
  });
  // szerokie tabele (6+ kolumn): długi tekst skrócony, pełna treść po najechaniu
  main.querySelectorAll("table").forEach(function (t) {
    var tr = t.querySelector("tbody tr");
    if (!tr || tr.children.length < 6) return;
    t.classList.add("szeroka");

    t.querySelectorAll("tbody tr").forEach(function (r) {
      var c0 = r.children[0];
      if (c0 && c0.textContent.trim().length <= 6) c0.classList.add("waska");
      Array.prototype.forEach.call(r.querySelectorAll("td"), function (c) {
        var txt = c.textContent.trim();
        if (txt.length > 20) { c.classList.add("dluga"); c.title = txt; }
      });
    });

    // nazwy typu FormalEducation -> "Formal" i "Education" w dwóch liniach
    t.querySelectorAll("thead th").forEach(function (h) {
      var n = h.textContent.trim();
      if (n.length > 8 && !/\s/.test(n)) h.innerHTML = n.replace(/([a-z])([A-Z])/g, "$1<br>$2");
    });

    t.querySelectorAll("thead th").forEach(function (h) {
      var n = h.textContent.trim();
      if (n === "Respondent" || n === "ID") h.classList.add("waska");
    });

    // ukryj pierwszą kolumnę z numerem wiersza (indeks), jeśli drugą jest ID
    var h2 = t.querySelectorAll("thead tr:first-child th")[1];
    if (h2 && h2.textContent.trim() === "ID") {
      t.querySelectorAll("tr").forEach(function (r) { if (r.children[0]) r.children[0].style.display = "none"; });
    }
  });

  // linie "Etykieta: wartość" z wydruków -> kafelki
  main.querySelectorAll("pre").forEach(function (p) {
    var linie = p.textContent.split("\n").map(function (l) { return l.trim(); }).filter(Boolean);
    var pary = [];
    linie.forEach(function (l) {
      l.split(" | ").forEach(function (czesc) {
        var m = czesc.match(/^(.+?)\s*[:=]\s*(.+)$/);
        if (m && m[2].length <= 40) pary.push([m[1], m[2]]);
      });
    });
    if (pary.length >= 2 && pary.length >= linie.length) {
      var d = document.createElement("div"); d.className = "kafle";
      pary.forEach(function (x) {
        var k = document.createElement("div"); k.className = "kafel";
        k.innerHTML = "<b></b><span></span>";
        k.querySelector("b").textContent = x[1]; k.querySelector("span").textContent = x[0];
        d.appendChild(k);
      });
      p.parentNode.replaceChild(d, p);
    }
  });
  // tabele w ramce z przewijaniem
  var wraps = [];
  main.querySelectorAll("table").forEach(function (t) {
    t.removeAttribute("border");
    var w = document.createElement("div"); w.className = "tab-wrap";
    t.parentNode.insertBefore(w, t); w.appendChild(t);
    wraps.push(w);
  });

  // małe tabele (do 4 kolumn) z sąsiednich komórek lub z jednej komórki idą obok siebie
  function komorka(w) { return w.closest(".jp-Cell, .cell"); }
  function male(w) { var tr = w.querySelector("tr"); return tr && tr.children.length <= 4; }
  var i = 0;
  while (i < wraps.length) {
    var grupa = [wraps[i]];
    var j = i + 1;
    while (j < wraps.length && male(wraps[j - 1]) && male(wraps[j])) {
      var c1 = komorka(wraps[j - 1]), c2 = komorka(wraps[j]);
      var ta_sama = c1 === c2;
      var sasiednia = c1 && c2 && c2.previousElementSibling === c1 && !c2.querySelector("pre, img");
      if (!(ta_sama || sasiednia)) break;
      grupa.push(wraps[j]); j++;
    }
    if (grupa.length > 1) {
      var rzad = document.createElement("div"); rzad.className = "tab-row";
      grupa[0].parentNode.insertBefore(rzad, grupa[0]);
      grupa.forEach(function (g) { rzad.appendChild(g); });
    }
    i = j;
  }
    // opisy "komentarz" i "Odpowiedź": mały przycisk, treść rozwija się po kliknięciu
  main.querySelectorAll("p").forEach(function (p) {
    var kont = p.parentNode;
    if (kont.firstElementChild !== p || kont.closest("details.odp")) return;   // akapit musi otwierać komórkę Markdown
    var t = p.textContent.trim();
    var etykieta = /^komentarz/i.test(t) ? "komentarz" : (/^Odpowiedź/i.test(t) ? "Odpowiedź" : null);
    if (!etykieta) return;
    var s = p.querySelector("strong");
    if (s) {
      if (etykieta === "komentarz") s.remove();
      else { var x = s.textContent.replace(/^Odpowiedź:\s*/i, ""); s.textContent = x.charAt(0).toUpperCase() + x.slice(1); }
    }
    var det = document.createElement("details"); det.className = "odp";
    var sum = document.createElement("summary"); sum.textContent = etykieta;
    var tresc = document.createElement("div"); tresc.className = "odp-tresc";
    while (kont.firstChild) tresc.appendChild(kont.firstChild);
    det.appendChild(sum); det.appendChild(tresc); kont.appendChild(det);
  });
  window.addEventListener("beforeprint", function () {
    main.querySelectorAll("details.odp").forEach(function (d) { d.open = true; });
  });
});
</script>
</body>
</html>
"""

html_out = (STRONA.replace("%%BOOTSTRAP%%", bootstrap)
            .replace("%%TYTUL%%", html.escape(TYTUL)).replace("%%PODTYTUL%%", html.escape(PODTYTUL))
            .replace("%%AUTOR%%", html.escape(AUTOR)).replace("%%DATA%%", date.today().strftime("%d.%m.%Y"))
            .replace("%%STRESZCZENIE%%", html.escape(STRESZCZENIE)).replace("%%SLOWA%%", html.escape(SLOWA))
            .replace("%%TRESC%%", tresc))

WYJSCIE.parent.mkdir(exist_ok=True)
WYJSCIE.write_text(html_out, encoding="utf-8")
print("Gotowe:", WYJSCIE.resolve())