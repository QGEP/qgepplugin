SELECT ab.obj_id AS bauwerk_obj_id,
    ab.detailgeometrie,
    ab.baujahr,
    ab.baulicherzustand,
    ab.baulos,
    ab.bemerkung AS abwasserbauwerk_bemerkung,
    ab.bezeichnung AS abwasserbauwerk_bezeichnung,
    ab.funktion,
    ab.standortname,
    ab.astatus,
    ab.zugaenglichkeit,
    ab.dimension1,
    ab.dimension2,
	ab.t_type,
	ab_text.plantyp,
	ab_text.textinhalt,
	ab_text.textpos,
	ab_text.textori,
	ab_text.texthali,
	ab_text.textvali,
	COALESCE(MAX(ab_nach.nutzungsart_ist), MAX(ab_von.nutzungsart_ist)) AS kanal_nutzungsart_ist
   FROM abwasser_test.abwasserbauwerk ab
     LEFT JOIN abwasser_test.abwassernetzelement an ON ab.t_id = an.abwasserbauwerkref
     LEFT JOIN abwasser_test.haltungspunkt hp ON an.t_id = hp.abwassernetzelementref
     LEFT JOIN abwasser_test.abwassernetzelement an_nach ON an_nach.vonhaltungspunktref = hp.t_id
     LEFT JOIN abwasser_test.abwasserbauwerk ab_nach ON ab_nach.t_id = an_nach.abwasserbauwerkref
     LEFT JOIN abwasser_test.abwassernetzelement an_von ON an_von.nachhaltungspunktref = hp.t_id
     LEFT JOIN abwasser_test.abwasserbauwerk ab_von ON ab_von.t_id = an_von.abwasserbauwerkref
	 LEFT JOIN abwasser_test.abwasserbauwerk_text ab_text ON ab_text.abwasserbauwerkref = ab.t_id
   WHERE an.t_type::text = 'abwasserknoten'::text AND ab.detailgeometrie IS NOT NULL
   GROUP BY
    ab.obj_id,
    ab.detailgeometrie,
    ab.baujahr,
    ab.baulicherzustand,
    ab.baulos,
    ab.bemerkung,
    ab.bezeichnung,
	ab.funktion,
    ab.standortname,
    ab.astatus,
    ab.zugaenglichkeit,
    ab.dimension1,
    ab.dimension2,
	ab.t_type,
	ab_text.plantyp,
	ab_text.textinhalt,
	ab_text.textpos,
	ab_text.textori,
	ab_text.texthali,
	ab_text.textvali

