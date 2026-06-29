from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB SPARQL 엔드포인트 연결
sparql = SPARQLWrapper("http://localhost:7200/repositories/aicc-demo")
sparql.setReturnFormat(JSON)

def graph_query(inquiry_type: str):
    query = f"""
    PREFIX aicc: <http://smartmind.ai/aicc#>
    SELECT ?처리단계 ?담당부서 ?연락처
    WHERE {{
      aicc:{inquiry_type} aicc:처리절차 ?처리단계 .
      ?처리단계 aicc:담당한다 ?담당부서 .
      ?담당부서 aicc:연락처 ?연락처 .
    }}
    """
    sparql.setQuery(query)
    results = sparql.query().convert()

    print(f"\n{'='*40}")
    print(f"고객 문의 유형: {inquiry_type}")
    print(f"{'='*40}")
    bindings = results["results"]["bindings"]
    if not bindings:
        print("  처리 정보 없음")
    for r in bindings:
        step  = r["처리단계"]["value"].split("#")[1]
        dept  = r["담당부서"]["value"].split("#")[1]
        phone = r["연락처"]["value"]
        print(f"  처리단계: {step}")
        print(f"  담당부서: {dept}")
        print(f"  연락처:   {phone}")

# 세 가지 문의 유형 테스트
graph_query("청구서문의")
graph_query("장애문의")
graph_query("해지문의")
