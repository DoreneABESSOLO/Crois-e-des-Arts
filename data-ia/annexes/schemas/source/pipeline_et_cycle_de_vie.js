// Pipeline de Cabine avant / après et cycle de vie de la donnée — source versionnée (pptxgenjs).
// Règles appliquées (how-to tech, étape 3) : mêmes étapes des deux côtés, orange = problème V1, bleu = mesure V2, une mesure = une source.
const pptxgen = require("pptxgenjs");
let applyTheme = async () => {}; // thème facultatif (couleurs déjà fixées dans le code)

// Palette reprise des fichiers du groupe
const THEME = {
  name: "FashMatch groupe",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1A1A1A", lt1: "FFFFFF", dk2: "1A1A1A", lt2: "F1EFE8",
    accent1: "0F6E56", accent2: "E1F5EE", accent3: "A32D2D", accent4: "FCEBEB",
    accent5: "5F5E5A", accent6: "2F6FB3", hlink: "2F6FB3", folHlink: "5F5E5A",
  },
};
const G = { fill: "E8F0FF", line: "0B5FFF", txt: "0B3F99" };   // encadré / mesure V2
const R = { fill: "FFF1E4", line: "E8710A", txt: "9A4A00" };   // problème V1
const N = { fill: "FFFFFF", line: "5F5E5A", txt: "5F5E5A" };   // acteur / traitement
const T = { fill: "FFFFFF", line: "8A8A8A", txt: "5F5E5A" };   // tiers
const ARROW = "5F5E5A";

function newDeck() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };
  const C = pres.SchemeColor;
  pres.defineSlideMaster({
    title: "Schéma",
    background: { color: "FFFFFF" },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.4, y: 0.22, w: 9.2, h: 0.55, fontSize: 22, bold: true, color: "1A1A1A", valign: "middle", align: "left" }, text: "" } },
    ],
  });
  return pres;
}

function box(s, pres, x, y, w, h, title, sub, p, opt = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.06, fill: { color: p.fill },
    line: { color: p.line, width: 1, dashType: opt.dash ? "dash" : "solid" }, objectName: "Bloc " + title,
  });
  const runs = [{ text: title, options: { bold: true, fontSize: opt.tsize || 11, color: "1A1A1A", breakLine: !!sub } }];
  if (sub) runs.push({ text: sub, options: { fontSize: opt.size || 8.5, color: p.txt } });
  s.addText(runs, { x: x + 0.05, y, w: w - 0.1, h, align: opt.align || "center", valign: opt.valign || "middle", margin: 2, isTextBox: true, paraSpaceAfter: 2 });
}

function can(s, pres, x, y, w, h, title, sub) {
  s.addShape(pres.shapes.CAN, { x, y, w, h, fill: { color: G.fill }, line: { color: G.line, width: 1 }, objectName: "Stockage " + title });
  s.addText([{ text: title, options: { bold: true, fontSize: 8.5, color: "1A1A1A", breakLine: true } }, { text: sub, options: { fontSize: 7.5, color: G.txt } }],
    { x, y: y + 0.08, w, h: h - 0.08, align: "center", valign: "middle", margin: 1, isTextBox: true });
}

function arrow(s, pres, x1, y1, x2, y2, label, opt = {}) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  s.addShape(pres.shapes.LINE, {
    x, y, w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001,
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: opt.color || ARROW, width: 1.25, endArrowType: opt.noHead ? undefined : "triangle", dashType: opt.dash ? "dash" : "solid" },
  });
  if (label) {
    s.addText(label, { x: opt.lx ?? (Math.min(x1, x2) - 0.15), y: opt.ly ?? (y - (opt.lh || 0.22) - 0.02), w: opt.lw ?? (Math.abs(x2 - x1) + 0.3), h: opt.lh || 0.22, valign: "bottom", fontSize: 7, italic: true, color: opt.color || ARROW, align: "center", margin: 0, isTextBox: true });
  }
}

function legend(s, pres, items, x, y) {
  items.forEach(([p, label, dash], k) => {
    s.addShape(label === "Acteur" ? pres.shapes.OVAL : pres.shapes.ROUNDED_RECTANGLE, { x, y: y + k * 0.27, w: label === "Acteur" ? 0.26 : 0.17, h: 0.17, rectRadius: 0.03, fill: { color: p.fill }, line: { color: p.line, width: 1, dashType: dash ? "dash" : "solid" } });
    s.addText(label, { x: x + (label === "Acteur" ? 0.34 : 0.24), y: y + k * 0.27 - 0.04, w: 2.4, h: 0.25, fontSize: 8, color: "333333", margin: 0, isTextBox: true });
  });
}

// =============================================================== Deck 1 : pipeline Cabine avant / après
const steps = [
  { t: "1. Import photo", out: "selfie" },
  { t: "2. Stockage", out: "selfie + tenue" },
  { t: "3. Génération", out: "image générée" },
  { t: "4. Partage", out: "photos, images" },
  { t: "5. Conservation", out: "photos" },
  { t: "6. Entraînement", out: null },
];
const V1 = [
  "N'importe quelle photo peut être importée, même celle d'une autre personne",
  "Photos stockées en clair, services en partie hors UE, accès non tracés",
  "Image réaliste avec toutes les tenues, maillots compris, sans filtre",
  "Partage sur les réseaux sans aucune mention IA",
  "Photos gardées 5 ans par défaut",
  "Photos réutilisées pour entraîner les modèles, sans accord",
];
const V2 = [
  ["Photo prise en direct avec la caméra + détection du vivant, accord explicite", "RGPD art. 6 · Omnibus IA"],
  ["Pas de stockage : photo traitée en mémoire. Chiffrement, serveurs UE", "RGPD art. 25, 32, chap. V"],
  ["Maillots et lingerie : essayage sur un avatar, jamais sur la vraie photo ; filtre sur les images produites", "Omnibus IA (nudification)"],
  ["Mention « Générée par IA » + marquage C2PA, partage désactivé par défaut", "AI Act art. 50"],
  ["Photo effacée tout de suite ; image générée : durée courte à fixer avec la DPO, purge automatique", "RGPD art. 5.1.e"],
  ["Seulement si opt-in, jeu séparé, données pseudonymisées", "RGPD art. 6 et 7"],
];

function pipelineSlide(pres, title, isV2) {
  const s = pres.addSlide({ masterName: "Schéma" });
  s.addText(title, { placeholder: "title" });
  // utilisateur
  s.addShape(pres.shapes.OVAL, { x: 0.4, y: 0.95, w: 1.35, h: 0.55, fill: { color: N.fill }, line: { color: N.line, width: 1 }, objectName: "Acteur Utilisateur" });
  s.addText("Utilisateur", { x: 0.4, y: 0.95, w: 1.35, h: 0.55, fontSize: 10, bold: true, color: "1A1A1A", align: "center", valign: "middle", margin: 0, isTextBox: true });
  arrow(s, pres, 1.75, 1.22, 2.35, 1.22, null);
  s.addText(isV2 ? "selfie pris en direct" : "n'importe quelle photo", { x: 1.85, y: 1.27, w: 1.3, h: 0.2, fontSize: 7, italic: true, color: ARROW, margin: 0, isTextBox: true });
  s.addText("Module Cabine, essayage virtuel", { x: 2.4, y: 1.02, w: 4, h: 0.4, fontSize: 10, bold: true, color: "333333", margin: 0, isTextBox: true });
  // 2 rangées de 3 étapes
  const W = 2.6, H = 1.35, GAP = 0.55, X0 = 0.6, Y = [1.6, 3.55];
  steps.forEach((st, i) => {
    const row = Math.floor(i / 3), col = i % 3;
    const x = X0 + col * (W + GAP), y = Y[row];
    const p = isV2 ? G : R;
    const sub = isV2 ? V2[i][0] : V1[i];
    box(s, pres, x, y, W, H, st.t, sub, p, { size: 9 });
    if (isV2) s.addText(V2[i][1], { x, y: y + H + 0.02, w: W, h: 0.22, fontSize: 7.5, italic: true, color: "5F5E5A", align: "center", margin: 0, isTextBox: true });
    // flèches dans la rangée
    if (col < 2) arrow(s, pres, x + W, y + H / 2, x + W + GAP, y + H / 2, (isV2 && i === 4) ? "si opt-in" : st.out, { lx: x + W + 0.02, lw: GAP - 0.04, lh: 0.32 });
  });
  // coude entre l'étape 3 et l'étape 4
  const x3 = X0 + 2 * (W + GAP) + W / 2, yb = Y[0] + H + (isV2 ? 0.26 : 0.04), ym = Y[0] + H + (isV2 ? 0.4 : 0.33), x4 = X0 + W / 2;
  arrow(s, pres, x3, yb, x3, ym, null, { noHead: true });
  arrow(s, pres, x3, ym, x4, ym, steps[2].out, { noHead: true, lx: x4 + 0.1, lw: 1.2, ly: ym - 0.26 });
  arrow(s, pres, x4, ym, x4, Y[1], null);
  legend(s, pres, isV2 ? [[G, "Mesure V2 (source en italique)"]] : [[R, "Point à risque"], [N, "Acteur"]], 7.2, 0.98);
  return s;
}

const p1 = newDeck();
pipelineSlide(p1, "Pipeline V1 : avant", false);
pipelineSlide(p1, "Pipeline V2 : après", true);

// =============================================================== Deck 2 : architecture + cycle de vie
const p2 = newDeck();
let s;
// ---------- cycle de vie avant / après
s = p2.addSlide({ masterName: "Schéma" });
s.addText("Cycle de vie de la donnée : avant / après", { placeholder: "title" });
const STEPS = ["Collecte", "Stockage", "Traitement", "Modèle", "Sortie", "Suppression"];
const CV1 = [
  "N'importe quelle photo\nVisage scanné pour l'âge\nTout est collecté",
  "Photos en clair\nEn partie hors UE\nAccès non tracés",
  "Croisement libre\nInsight déduit religion, orientation, origine",
  "Entraîné sur les données des premiers clients, sans accord",
  "Images sans mention\nStella se dit humaine\nRefus sans motif",
  "5 ans par défaut\npour toutes les données",
];
const CV2 = [
  ["Champs utiles seulement\nPhoto prise en direct\nConsentement par finalité", "RGPD art. 5, 7, 25"],
  ["Photos non stockées\nChiffré, serveurs UE\nAccès limités et journalisés", "RGPD art. 32, chap. V"],
  ["Données pseudonymisées\nInsight retiré", "RGPD art. 9 · AI Act art. 5"],
  ["Jeu séparé, opt-in\nContrôle des biais", "RGPD art. 6 · ISO 42001"],
  ["Mention IA + C2PA\nStella annoncée comme IA\nMotif + recours humain", "AI Act art. 50 · RGPD art. 22"],
  ["Photos : tout de suite\nImages, conversations : durée courte (DPO)\nNavigation : 13 mois\nComptes inactifs : 3 ans", "RGPD art. 5.1.e, 17"],
];
const CX0 = 0.9, CW = 1.42, CG = 0.08;
STEPS.forEach((t, i) => {
  const x = CX0 + i * (CW + CG);
  s.addShape(p2.shapes.CHEVRON, { x, y: 0.95, w: CW + 0.06, h: 0.42, fill: { color: "F2F2F2" }, line: { color: "8A8A8A" }, objectName: "Étape " + t });
  s.addText(t, { x: x + 0.12, y: 0.95, w: CW - 0.12, h: 0.42, fontSize: 9.5, bold: true, color: "1A1A1A", align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addShape(p2.shapes.ROUNDED_RECTANGLE, { x, y: 1.5, w: CW, h: 1.45, rectRadius: 0.05, fill: { color: R.fill }, line: { color: R.line, width: 1 } });
  s.addText(CV1[i], { x: x + 0.04, y: 1.5, w: CW - 0.08, h: 1.45, fontSize: 8.5, color: R.txt, align: "center", valign: "middle", margin: 2, isTextBox: true });
  s.addShape(p2.shapes.ROUNDED_RECTANGLE, { x, y: 3.1, w: CW, h: 1.75, rectRadius: 0.05, fill: { color: G.fill }, line: { color: G.line, width: 1 } });
  s.addText(CV2[i][0], { x: x + 0.04, y: 3.1, w: CW - 0.08, h: 1.75, fontSize: 8.5, color: G.txt, align: "center", valign: "middle", margin: 2, isTextBox: true });
  s.addText(CV2[i][1], { x, y: 4.9, w: CW, h: 0.3, fontSize: 7.5, italic: true, color: "5F5E5A", align: "center", margin: 0, isTextBox: true });
});
[["V1", R, 1.5, 1.45], ["V2", G, 3.1, 1.75]].forEach(([t, p, y, h]) => {
  s.addShape(p2.shapes.ROUNDED_RECTANGLE, { x: 0.3, y, w: 0.5, h, rectRadius: 0.05, fill: { color: p.line }, line: { color: p.line } });
  s.addText(t, { x: 0.3, y, w: 0.5, h, fontSize: 13, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
});
s.addText("Orange : problème V1 · bleu : mesure V2 · en italique : la règle qui la justifie", { x: 0.3, y: 5.22, w: 7, h: 0.25, fontSize: 8, italic: true, color: "5F5E5A", margin: 0, isTextBox: true });

(async () => {
  const out1 = process.argv[2] || "pipeline_cabine_avant_apres.pptx";
  const out2 = process.argv[3] || "cycle_de_vie_avant_apres.pptx";
  await p1.writeFile({ fileName: out1 });
  await p2.writeFile({ fileName: out2 });
  await applyTheme(out1, THEME);
  await applyTheme(out2, THEME);
  console.log("ok");
})();
