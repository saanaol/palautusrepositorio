import unittest
from unittest.mock import Mock, ANY, call
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_yhden_tuotteen_maksutiedot_ovat_oikein(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()
        varasto_mock.saldo.return_value = 10
        varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 5
        )

    def test_kahden_eri_tuotteen_maksutiedot_ovat_oikein(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42

        tuotteet = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "leipa", 3)
        }

        varasto_mock = Mock()
        varasto_mock.saldo.return_value = 10
        varasto_mock.hae_tuote.side_effect = tuotteet.get

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 8
        )

    def test_kahden_saman_tuotteen_maksutiedot_ovat_oikein(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()
        varasto_mock.saldo.return_value = 10
        varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 10
        )

    def test_loppunutta_tuotetta_ei_laskuteta(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42

        tuotteet = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "leipa", 3)
        }
        saldot = {
            1: 10,
            2: 0
        }

        varasto_mock = Mock()
        varasto_mock.saldo.side_effect = saldot.get
        varasto_mock.hae_tuote.side_effect = tuotteet.get

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 5
        )

    def test_uusi_asiointi_nollaa_edellisen_ostoksen(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()
        varasto_mock.saldo.return_value = 10
        varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(
            pankki_mock.tilisiirto.call_args_list,
            [
                call("pekka", ANY, "12345", "33333-44455", 10),
                call("pekka", ANY, "12345", "33333-44455", 5)
            ]
        )

    def test_jokaiselle_maksulle_pyydetaan_uusi_viite(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.side_effect = [42, 43]

        varasto_mock = Mock()
        varasto_mock.saldo.return_value = 10
        varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        for _ in range(2):
            kauppa.aloita_asiointi()
            kauppa.lisaa_koriin(1)
            kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 2)

        self.assertEqual(
            pankki_mock.tilisiirto.call_args_list,
            [
                call("pekka", 42, "12345", "33333-44455", 5),
                call("pekka", 43, "12345", "33333-44455", 5)
            ]
        )

    def test_poistettu_tuote_ei_nay_maksussa_ja_palautuu_varastoon(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42

        tuote = Tuote(1, "maito", 5)

        varasto_mock = Mock()
        varasto_mock.saldo.return_value = 10
        varasto_mock.hae_tuote.return_value = tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.poista_korista(1)
        kauppa.tilimaksu("pekka", "12345")

        varasto_mock.palauta_varastoon.assert_called_once_with(tuote)

        pankki_mock.tilisiirto.assert_called_once_with(
            "pekka", ANY, "12345", "33333-44455", 0
        )
