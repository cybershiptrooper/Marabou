/*********************                                                        */
/*! \file Test_SparseConstraintMatrixAnalyzer.h
 ** \verbatim
 ** Top contributors (to current version):
 **   Guy Katz, Shantanu Thakoor
 ** This file is part of the Marabou project.
 ** Copyright (c) 2017-2019 by the authors listed in the file AUTHORS
 ** in the top-level source directory) and their institutional affiliations.
 ** All rights reserved. See the file COPYING in the top-level source
 ** directory for licensing information.\endverbatim
 **
 ** \brief [[ Add one-line brief description here ]]
 **
 ** [[ Add lengthier description here ]]
 **/

#include <cxxtest/TestSuite.h>

#include "SparseConstraintMatrixAnalyzer.h"

#include <string.h>
#include <cstdio>

class MockForSparseConstraintMatrixAnalyzer
{
public:
};

class SparseConstraintMatrixAnalyzerTestSuite : public CxxTest::TestSuite
{
public:
	MockForSparseConstraintMatrixAnalyzer *mock;

	void setUp()
	{
		TS_ASSERT( mock = new MockForSparseConstraintMatrixAnalyzer );
	}

	void tearDown()
	{
		TS_ASSERT_THROWS_NOTHING( delete mock );
	}

    void test_analyze__gaussian_eliminiation()
    {
        double result[15];

        {
            double A1[] = {
                1, 0, 0, 0, 0,
                0, 0, 1, 0, 0,
                0, 0, 0, 1, 0,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                1, 0, 0, 0, 0,
                0, 1, 0, 0, 0,
                0, 0, 1, 0, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 3U );
            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                1, 0, 0, 0, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 1, 0,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                1, 0, 0, 0, 0,
                0, 1, 0, 0, 0,
                0, 0, 1, 1, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 3U );

            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                1, 0, 0, 0, 0,
                1, 0, 0, 0, 0,
                0, 1, 0, 2, 0,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                2, 0, 0, 1, 0,
                0, 1, 0, 0, 0,
                0, 0, 0, 0, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 2U );

            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                1, 1, 0, 1, 0,
                0, 0, 3, 0, 0,
                2, 2, 0, 0, 0,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                3, 0, 0, 0, 0,
                0, 2, 0, 2, 0,
                0, 0, 1, 0, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 3U );

            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                15, 3,  0, 1, 0,
                0 , 0, -1, 1, 4,
                15, 3, -1, 2, 4,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                15, 0,  0, 1, 3,
                0 , 4, -1, 1, 0,
                0 , 0,  0, 0, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 2U );

            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 0U );

            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 2, 3, 14, 1,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                14, 2, 3, 0, 1,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 1U );

            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            // Test when initialized from sparse lists

            double A1[] = {
                1, 0, 0, 0, 0,
                1, 0, 0, 0, 0,
                0, 1, 0, 2, 0,
            };

            SparseUnsortedList *matrix[3];
            matrix[0] = new SparseUnsortedList( A1, 5 );
            matrix[1] = new SparseUnsortedList( A1 + 5, 5 );
            matrix[2] = new SparseUnsortedList( A1 + 10, 5 );

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( matrix, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            double expectedResult[] = {
                2, 0, 0, 1, 0,
                0, 1, 0, 0, 0,
                0, 0, 0, 0, 0,
            };

            TS_ASSERT_THROWS_NOTHING( analyzer->getCanonicalForm( result ) );
            TS_ASSERT_SAME_DATA( result, expectedResult, sizeof(expectedResult) );
            TS_ASSERT_EQUALS( analyzer->getRank(), 2U );

            TS_ASSERT_THROWS_NOTHING( delete analyzer );

            delete matrix[0];
            delete matrix[1];
            delete matrix[2];
        }
    }

    void test_independent_columns()
    {
        {
            double A1[] = {
                1, 0, 0, 0, 0,
                0, 1, 0, 0, 0,
                0, 0, 1, 0, 0,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            List<unsigned> cols = analyzer->getIndependentColumns();
            TS_ASSERT_EQUALS( cols.size(), 3U );
            auto it = cols.begin();
            TS_ASSERT_EQUALS( *it, 0U );
            ++it;
            TS_ASSERT_EQUALS( *it, 1U );
            ++it;
            TS_ASSERT_EQUALS( *it, 2U );
            ++it;
            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                0, 1, 0, 0, 0,
                0, 0, 1, 1, 0,
                0, 0, 0, 0, 1,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            List<unsigned> cols = analyzer->getIndependentColumns();
            TS_ASSERT_EQUALS( cols.size(), 3U );
            auto it = cols.begin();
            TS_ASSERT_EQUALS( *it, 1U );
            ++it;
            TS_ASSERT_EQUALS( *it, 2U );
            ++it;
            TS_ASSERT_EQUALS( *it, 4U );
            ++it;
            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }

        {
            double A1[] = {
                1, 0, 0, 0, 0,
                0, 1, 1, 1, 0,
                0, 0, 0, 0, 1,
            };

            SparseConstraintMatrixAnalyzer *analyzer;
            TS_ASSERT( analyzer = new SparseConstraintMatrixAnalyzer( A1, 3, 5 ) );

            TS_ASSERT_THROWS_NOTHING( analyzer->analyze() );

            List<unsigned> cols = analyzer->getIndependentColumns();
            TS_ASSERT_EQUALS( cols.size(), 3U );
            auto it = cols.begin();
            TS_ASSERT_EQUALS( *it, 0U );
            ++it;
            TS_ASSERT_EQUALS( *it, 1U );
            ++it;
            TS_ASSERT_EQUALS( *it, 4U );
            ++it;
            TS_ASSERT_THROWS_NOTHING( delete analyzer );
        }
    }
};

//
// Local Variables:
// compile-command: "make -C ../../.. "
// tags-file-name: "../../../TAGS"
// c-basic-offset: 4
// End:
//
