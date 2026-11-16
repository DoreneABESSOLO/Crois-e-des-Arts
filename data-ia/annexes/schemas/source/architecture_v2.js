// Schéma d'architecture conforme FashMatch V2 — source versionnée (pptxgenjs).
// Règles appliquées (how-to tech, étape 4) : une boîte = un composant, chaque flèche porte une donnée,
// frontières visibles, 5 couches, transverse dessiné, module retiré absent, légende commune à la carte des flux.
const pptxgen = require("pptxgenjs");

const P = { fill: "FFFFFF", line: "5F5E5A", txt: "5F5E5A" };   // traitement / stockage (neutre)
const A = { fill: "FFFFFF", line: "5F5E5A", txt: "5F5E5A" };   // acteur
const T = { fill: "FFFFFF", line: "8A8A8A", txt: "5F5E5A" };   // tiers externe
const ARR = "4A4A4A";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

function label(x, y, w, h, text, o = {}) {
  s.addText(text, { x, y, w, h, fontFace: "Arial", fontSize: o.size || 6.5, italic: o.italic !== false, bold: !!o.bold,
    color: o.color || ARR, align: o.align || "center", valign: o.valign || "middle", margin: 0, isTextBox: true });
}
function comp(x, y, w, h, title, sub, p = P, shape = "proc", o = {}) {
  const shapes = { proc: pres.shapes.ROUNDED_RECTANGLE, actor: pres.shapes.OVAL, tier: pres.shapes.HEXAGON, store: pres.shapes.CAN };
  const opt = { x, y, w, h, fill: { color: p.fill }, line: { color: p.line, width: 1.1, dashType: shape === "tier" ? "dash" : "solid" }, objectName: title };
  if (shape === "proc") opt.rectRadius = 0.06;
  s.addShape(shapes[shape], opt);
  const runs = [{ text: title, options: { bold: true, fontSize: o.t || 9, color: "1A1A1A", breakLine: !!sub } }];
  if (sub) runs.push({ text: sub, options: { fontSize: o.s || 6.8, color: p.txt } });
  const yy = shape === "store" ? y + h * 0.12 : y;
  s.addText(runs, { x: x + 0.04, y: yy, w: w - 0.08, h: shape === "store" ? h * 0.88 : h, fontFace: "Arial", align: "center", valign: "middle", margin: 1, isTextBox: true });
}
function line(x1, y1, x2, y2, o = {}) {
  s.addShape(pres.shapes.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001,
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: o.color || ARR, width: o.width || 1.1, endArrowType: o.noHead ? undefined : "triangle", beginArrowType: o.both ? "triangle" : undefined, dashType: o.dash || "solid" },
  });
}
function zone(x, y, w, h, color, name) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: "FFFFFF", transparency: 100 }, line: { color, width: 1.4, dashType: "dash" }, objectName: name });
}

// Titre
s.addText("Architecture conforme FashMatch V2", { x: 0.2, y: 0.18, w: 9, h: 0.5, fontFace: "Arial", fontSize: 22, bold: true, color: "1A1A1A", margin: 0 });

// Couches
[["1 · Accès", 0.15, 1.5], ["2 · Passerelle", 1.9, 1.85], ["3 · Services", 4.2, 2.3], ["4 · Données", 6.9, 2.05], ["5 · Tiers", 10.5, 2.65]].forEach(([t, x, w]) => {
  s.addShape(pres.shapes.RECTANGLE, { x, y: 0.82, w, h: 0.3, fill: { color: "F2F2F2" }, line: { color: "8A8A8A" }, objectName: "Couche " + t });
  s.addText(t, { x, y: 0.82, w, h: 0.3, fontFace: "Arial", fontSize: 10, bold: true, color: "1A1A1A", align: "center", valign: "middle", margin: 0 });
});

// Frontières
zone(0.12, 2.12, 1.5, 1.45, "8A8A8A", "Zone publique");
label(0.12, 3.3, 1.5, 0.22, "Zone publique", { italic: false, bold: true, color: "5F5E5A", size: 7 });
zone(1.82, 1.2, 7.25, 5.3, "5F5E5A", "Zone protégée UE");
label(4.2, 1.21, 4.85, 0.2, "Zone protégée FashMatch · région UE · données chiffrées (KMS au repos, TLS 1.3 en transit)", { italic: false, bold: true, color: "333333", size: 7, align: "right" });
zone(10.42, 1.2, 2.8, 4.25, "8A8A8A", "Hors de FashMatch");
label(10.42, 5.2, 2.8, 0.22, "Hors de FashMatch · tiers sous contrat (RGPD art. 28)", { italic: false, bold: true, color: "5F5E5A", size: 7 });

// 1 · Accès
comp(0.22, 1.45, 1.3, 0.5, "Utilisateur", "15 ans et +", A, "actor", { t: 8.5 });
line(0.87, 1.95, 0.87, 2.35);
label(0.9, 1.96, 0.75, 0.3, "saisies,\nselfie, messages", { align: "left", size: 6 });
comp(0.22, 2.35, 1.3, 0.75, "App mobile / web", "bandeau « IA », notices", P, "proc", { t: 8.5, s: 6.3 });

// 2 · Passerelle
comp(1.95, 1.45, 1.75, 3.15, "API Gateway", "authentification\n\nquotas anti-abus\n\nne laisse passer que les champs utiles à chaque finalité", P, "proc", { t: 10, s: 7 });
line(1.52, 2.72, 1.95, 2.72);
label(1.5, 2.43, 0.47, 0.28, "données\nsaisies", { size: 5.8 });
comp(1.95, 4.95, 1.4, 0.5, "Registre des consentements", "horodaté", P, "store", { t: 7.5, s: 6.3 });
line(2.65, 4.6, 2.65, 4.95);
label(2.7, 4.62, 0.95, 0.3, "choix de\nconsentement", { align: "left", size: 6 });

// 3 · Services
const SX = 4.25, SW = 2.2, SH = 0.5;
const SV = [
  ["Match", "recommandation, profilage sur opt-in", "clics,\nachats"],
  ["Contrôle d'âge", "âge déclaré + estimation en mémoire", "photo, âge\ndéclaré"],
  ["Cabine", "capture en direct · maillots, lingerie sur avatar · C2PA", "selfie\nen direct"],
  ["Pay3x", "orchestration, aucun score calculé", "panier"],
  ["Droits des personnes", "accès, export, effacement", "demande\nde droits"],
  ["Stella (IA déclarée)", "masquage des données sensibles", "message"],
];
const sy = (i) => 1.45 + i * 0.65;
const sc = (i) => sy(i) + SH / 2;
SV.forEach(([t, d, lab], i) => {
  comp(SX, sy(i), SW, SH, t, d, P, "proc", { t: 9, s: 6.5 });
  line(3.7, sc(i), SX, sc(i));
  label(3.71, sy(i) - 0.06, 0.53, 0.28, lab, { size: 5.8 });
});

// 4 · Données
const DX = 6.95, DW = 1.95;
comp(DX, 1.45, DW, 0.45, "Profils pseudonymisés", "user_id · 3 ans d'inactivité", P, "store", { t: 8, s: 6.3 });
line(SX + SW, sc(0), DX, 1.68);
label(6.45, 1.42, 0.5, 0.26, "user_id,\npréférences", { size: 5.6 });
line(SX + SW, sc(1) - 0.05, DX, 1.88);
label(6.45, 2.22, 0.5, 0.26, "oui / non\n15 ans et +", { size: 5.6 });
comp(DX, 2.03, DW, 0.45, "Jeu d'entraînement", "séparé · profils et conversations si opt-in", P, "store", { t: 8, s: 6 });
line(7.4, 1.9, 7.4, 2.03);
label(7.45, 1.88, 0.6, 0.16, "si opt-in", { align: "left", size: 5.6 });
comp(DX, 2.78, DW, 0.45, "Images générées", "chiffrées · durée courte (à fixer avec la DPO)", P, "store", { t: 8, s: 6.3 });
line(SX + SW, sc(2), DX, sc(2));
label(6.45, sc(2) - 0.28, 0.5, 0.26, "image\nmarquée", { size: 5.6 });
comp(DX, 4.07, 0.93, 0.47, "Coffre de pseudonymisation", null, P, "store", { t: 6.3 });
comp(DX + 1.02, 4.07, 0.93, 0.47, "Zone identité", "e-mail", P, "store", { t: 6.8, s: 6 });
line(DX + 0.93, 4.33, DX + 1.02, 4.33);
line(SX + SW, sc(4), DX, 4.3);
label(6.45, 4.0, 0.5, 0.26, "jeton", { size: 5.6 });
comp(DX, 5.1, DW, 0.45, "Conversations", "durée courte (à fixer avec la DPO)", P, "store", { t: 8, s: 6.3 });
line(SX + SW, sc(5) + 0.12, DX, 5.3);
label(6.42, 5.15, 0.55, 0.26, "conversation", { size: 5.6 });

// 5 · Tiers
const TX = 10.55, TW = 2.55;
comp(TX, 1.42, TW, 0.52, "Hébergeur cloud", "régions UE uniquement", T, "tier", { t: 8.5, s: 6.5 });
line(DX + DW, 1.68, TX, 1.68);
label(8.95, 1.42, 1.55, 0.24, "données chiffrées (hébergement)", { size: 5.8 });
comp(TX, 2.74, TW, 0.52, "Réseaux sociaux", "partage manuel", T, "tier", { t: 8.5, s: 6.5 });
line(DX + DW, sc(2), TX, sc(2));
label(8.95, 2.74, 1.55, 0.24, "image + mention IA, si partage", { size: 5.8 });
comp(TX, 3.39, TW, 0.52, "Prestataire de paiement", "agréé · vérifie les 18 ans · décide", T, "tier", { t: 8.5, s: 6.3 });
line(SX + SW, sc(3) - 0.07, TX, sc(3) - 0.07);
label(8.95, sc(3) - 0.32, 1.55, 0.22, "panier + jeton client", { size: 5.8 });
line(TX, sc(3) + 0.08, SX + SW, sc(3) + 0.08);
label(8.95, sc(3) + 0.1, 1.55, 0.22, "accord / refus + motif", { size: 5.8 });
comp(TX, 4.69, TW, 0.52, "Fournisseur du modèle d'IA", "endpoint UE · aucune conservation", T, "tier", { t: 8.5, s: 6.3 });
line(SX + SW, sc(5) - 0.02, TX, sc(5) - 0.02);
label(8.95, sc(5) - 0.26, 1.55, 0.22, "message masqué, sans identifiant", { size: 5.8 });

// Transverse
label(1.95, 5.5, 2.5, 0.2, "Transverse", { italic: false, bold: true, color: "333333", size: 8, align: "left" });
const TRY = 5.75, TRH = 0.6, TRW = 1.3;
comp(1.95, TRY, TRW, TRH, "Console interne", "file de revue des contestations", P, "proc", { t: 8, s: 6.2 });
comp(3.37, TRY, TRW, TRH, "Gestion des accès", "rôles, moindre privilège, MFA", P, "proc", { t: 8, s: 6.2 });
comp(4.79, TRY, TRW, TRH, "Gestion des clés", "KMS · rotation annuelle", P, "proc", { t: 8, s: 6.2 });
comp(6.21, TRY, TRW, TRH, "Journal d'audit", "protégé en écriture · 12 mois", P, "store", { t: 8, s: 6.2 });
comp(7.63, TRY, TRW, TRH, "Purge planifiée", "applique les durées de la zone 4", P, "proc", { t: 8, s: 6.2 });
line(5.4, sy(5) + SH, 6.7, TRY);
label(5.0, 5.45, 0.8, 0.26, "traces : qui,\nquoi, quand", { size: 5.6, align: "right" });
line(3.2, TRY, 4.25, sy(3) + SH);
label(3.6, 5.24, 0.66, 0.26, "réexamen humain\n(Âge, Pay3x)", { size: 5.6, align: "left" });

// Acteurs internes
comp(0.15, 5.55, 1.3, 0.45, "Équipe FashMatch", null, A, "actor", { t: 7.5 });
line(1.45, 5.82, 1.95, 5.92);
label(1.4, 5.5, 0.6, 0.26, "accès\nnominatif", { size: 5.6 });
comp(0.15, 6.3, 1.3, 0.45, "Réviseur humain", null, A, "actor", { t: 7.5 });
line(1.45, 6.45, 1.95, 6.2);
label(1.4, 6.48, 0.6, 0.26, "contestation\ntraitée", { size: 5.6 });

// Légende (commune à la carte des flux)
const LX = 9.4, LY = 5.62;
label(LX, LY, 3.6, 0.2, "Légende", { italic: false, bold: true, color: "1A1A1A", size: 8, align: "left" });
const items = [["actor", A, "Acteur"], ["proc", P, "Traitement"], ["store", P, "Stockage"], ["tier", T, "Tiers externe"]];
items.forEach(([sh, p, t], k) => {
  const x = LX + (k % 2) * 1.8, y = LY + 0.27 + Math.floor(k / 2) * 0.38;
  comp(x, y, 0.42, 0.28, "", null, p, sh);
  label(x + 0.5, y, 1.25, 0.28, t, { italic: false, align: "left", size: 7.5, color: "333333" });
});
line(LX, 6.75, LX + 0.42, 6.75);
label(LX + 0.5, 6.64, 3.2, 0.22, "Flèche : porte la donnée transportée", { italic: false, align: "left", size: 7.5, color: "333333" });
s.addShape(pres.shapes.RECTANGLE, { x: LX, y: 6.98, w: 0.42, h: 0.2, fill: { color: "FFFFFF" }, line: { color: "5F5E5A", width: 1.2, dashType: "dash" } });
label(LX + 0.5, 6.97, 3.3, 0.22, "Pointillés : frontière (UE, FashMatch, zone publique)", { italic: false, align: "left", size: 7.5, color: "333333" });

pres.writeFile({ fileName: process.argv[2] || "architecture_v2.pptx" }).then(() => console.log("ok"));
