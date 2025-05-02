% Dynamic facts
:- dynamic gejala_pos/1.
:- dynamic gejala_neg/1.

% Daftar penyakit
penyakit("Konjungtivitis").
penyakit("Katarak").
penyakit("Glaukoma").
penyakit("Mata Kering").
penyakit("Miopia").

% Basis Pengetahuan: Gejala untuk masing-masing penyakit
gejala(mata_merah, "Konjungtivitis").
gejala(gatal, "Konjungtivitis").
gejala(mata_berair, "Konjungtivitis").
gejala(mata_buram, "Katarak").
gejala(silau, "Katarak").
gejala(penglihatan_ganda, "Katarak").
gejala(nyeri_mata, "Glaukoma").
gejala(sakit_kepala, "Glaukoma").
gejala(penglihatan_teropong, "Glaukoma").
gejala(mata_kering, "Mata Kering").
gejala(terasa_sensitif, "Mata Kering").
gejala(mata_terbakar, "Mata Kering").
gejala(penglihatan_jauh_buram, "Miopia").
gejala(sakit_kepala, "Miopia").
gejala(menyipitkan_mata, "Miopia").

% Pertanyaan gejala
pertanyaan(mata_merah, "Apakah mata Anda merah?").
pertanyaan(gatal, "Apakah mata Anda terasa gatal?").
pertanyaan(mata_berair, "Apakah mata Anda sering berair?").
pertanyaan(mata_buram, "Apakah penglihatan Anda tampak buram?").
pertanyaan(silau, "Apakah Anda silau saat melihat cahaya terang?").
pertanyaan(penglihatan_ganda, "Apakah Anda melihat ganda?").
pertanyaan(nyeri_mata, "Apakah Anda merasakan nyeri pada mata?").
pertanyaan(sakit_kepala, "Apakah Anda sering sakit kepala?").
pertanyaan(penglihatan_teropong, "Apakah Anda merasa penglihatan seperti melalui terowongan?").
pertanyaan(mata_kering, "Apakah mata Anda terasa kering?").
pertanyaan(terasa_sensitif, "Apakah mata Anda sensitif terhadap cahaya/angin?").
pertanyaan(mata_terbakar, "Apakah mata terasa seperti terbakar?").
pertanyaan(penglihatan_jauh_buram, "Apakah Anda kesulitan melihat benda jauh dengan jelas?").
pertanyaan(menyipitkan_mata, "Apakah Anda sering menyipitkan mata untuk melihat dengan jelas?").

% Prosedur mengecek gejala
cek_gejala(G) :-
    gejala_pos(G), !.

cek_gejala(G) :-
    gejala_neg(G), !, fail.

cek_gejala(G) :-
    pertanyaan(G, T),
    write(T), nl,
    read(Jawaban),
    ( (Jawaban == ya ; Jawaban == y) ->
        assertz(gejala_pos(G));
        assertz(gejala_neg(G)), fail).

% Cocokkan semua gejala untuk penyakit
cocok_semua([]).
cocok_semua([H|T]) :-
    cek_gejala(H),
    cocok_semua(T).

% Diagnosis penyakit berdasarkan gejala
diagnosa(Penyakit) :-
    penyakit(Penyakit),
    findall(G, gejala(G, Penyakit), DaftarGejala),
    cocok_semua(DaftarGejala).

% Memulai sistem
mulai :-
    retractall(gejala_pos(_)),
    retractall(gejala_neg(_)),
    write('=== SISTEM DIAGNOSA PENYAKIT MATA ==='), nl,
    diagnosa(P),
    nl, write('Hasil diagnosa: Kemungkinan Anda mengalami: '), write(P), nl, !.

mulai :-
    write('Maaf, tidak dapat menentukan jenis penyakit mata berdasarkan gejala Anda.'), nl.
